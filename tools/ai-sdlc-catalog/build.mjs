#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import process from 'node:process';
import { pathToFileURL } from 'node:url';

export const BUILDER_SCHEMA = 'TASK-DESIGN-001-R019-Builder/v1';
export const SOURCE_SCHEMA = 'AI-SDLC-CatalogCompactSource/R019/v1';
export const CATALOG_SCHEMA = 'AI-SDLC-Catalog/R019/v1';
export const FORMAL_SOURCE_PATH = '.factory/catalog/ai-sdlc-catalog.source.json';
export const ACCEPTED_SOURCE_BASENAMES = Object.freeze([
  'ai-sdlc-catalog.source.json',
  'ai-sdlc-catalog.R019.source.json',
]);

function shaBuffer(buffer) {
  return crypto.createHash('sha256').update(buffer).digest('hex');
}

function fail(message) {
  const error = new Error(message);
  error.code = 'R019_SOURCE_CONTRACT_INVALID';
  throw error;
}

export function validateSource(source) {
  if (!source || typeof source !== 'object' || Array.isArray(source)) fail('source must be an object');
  if (source.schema_id !== SOURCE_SCHEMA) fail(`unexpected schema_id: ${source.schema_id}`);
  if (source.candidate_revision !== 'TASK-DESIGN-001-R019') fail('candidate revision mismatch');
  if (source.gate_generation !== 'TASK-DESIGN-001-R019-G001') fail('gate generation mismatch');
  if (source.formal_binding?.formal_requirements_version !== 'v4.0.0') fail('formal requirements version mismatch');
  const ids = source.workflow_inventory?.workflow_ids;
  if (!Array.isArray(ids) || ids.length !== 123 || new Set(ids).size !== 123) fail('workflow identity inventory must contain 123 unique IDs');
  if ((source.workflow_inventory?.semantic_workflow_additions || []).length !== 0) fail('semantic workflow additions are forbidden');
  if (!source.visibility_contract || !Array.isArray(source.requirement_mappings)) fail('visibility contract or requirement mappings missing');
  return source;
}

export function buildCatalogFromSourceObject(source, sourceBytes, sourceSha256) {
  validateSource(source);
  const records = [];
  records.push({
    record_type: 'catalog_metadata',
    record_id: 'META-AI-SDLC-CATALOG-R019',
    schema_version: '1.0.0-candidate',
    candidate_revision: source.candidate_revision,
    gate_generation: source.gate_generation,
    formal_binding: source.formal_binding,
    workflow_count: source.workflow_inventory.count,
    source_sha256: sourceSha256,
    source_bytes: sourceBytes,
  });
  for (const workflowId of source.workflow_inventory.workflow_ids) {
    records.push({
      record_type: 'workflow',
      record_id: workflowId,
      identity_status: 'retained_from_R017',
      visibility_contract_owner: source.workflow_inventory.affected_workflow_ids.includes(workflowId),
      provenance: { source_revision: source.candidate_revision, source_pointer: `/workflow_inventory/workflow_ids/${source.workflow_inventory.workflow_ids.indexOf(workflowId)}` },
    });
  }
  for (const [contractKey, contract] of Object.entries(source.visibility_contract)) {
    records.push({
      record_type: 'visibility_contract',
      record_id: contract.record_id || `VIS-${contractKey.toUpperCase().replaceAll('_', '-')}`,
      contract_key: contractKey,
      contract,
      provenance: { source_revision: source.candidate_revision, source_pointer: `/visibility_contract/${contractKey}` },
    });
  }
  for (const mapping of source.requirement_mappings) {
    records.push({
      record_type: 'coverage_mapping',
      record_id: `COV-R019-${mapping.requirement_id}`,
      ...mapping,
      provenance: { source_revision: source.candidate_revision, source_pointer: `/requirement_mappings/${source.requirement_mappings.indexOf(mapping)}` },
    });
  }
  for (const [family, seeds] of Object.entries(source.test_seeds || {})) {
    for (const seed of seeds) {
      records.push({
        record_type: 'test_case_seed',
        record_id: `R019-${family}-${records.filter((item) => item.record_type === 'test_case_seed' && item.family === family).length + 1}`,
        family,
        seed,
        provenance: { source_revision: source.candidate_revision, source_pointer: `/test_seeds/${family}` },
      });
    }
  }
  const recordTypeCounts = Object.fromEntries([...new Set(records.map((record) => record.record_type))].sort().map((recordType) => [recordType, records.filter((record) => record.record_type === recordType).length]));
  return {
    schema_id: CATALOG_SCHEMA,
    schema_version: '1.0.0-candidate',
    candidate_revision: source.candidate_revision,
    gate_generation: source.gate_generation,
    source_binding: { schema_id: source.schema_id, sha256: sourceSha256, bytes: sourceBytes },
    build_contract: { schema_id: BUILDER_SCHEMA, deterministic: true, network_reads: 0, child_processes: 0, external_persistent_writes: 0 },
    inventory: { records: records.length, workflows: recordTypeCounts.workflow, record_type_counts: recordTypeCounts },
    records,
  };
}

export function buildFromPaths(sourcePath, outputPath) {
  if (!ACCEPTED_SOURCE_BASENAMES.includes(path.basename(sourcePath))) {
    fail(`source basename must be one of: ${ACCEPTED_SOURCE_BASENAMES.join(', ')}`);
  }
  const sourceBuffer = fs.readFileSync(sourcePath);
  const source = JSON.parse(sourceBuffer.toString('utf8'));
  const catalog = buildCatalogFromSourceObject(source, sourceBuffer.length, shaBuffer(sourceBuffer));
  const output = `${JSON.stringify(catalog, null, 2)}\n`;
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, output, { encoding: 'utf8', flag: 'wx' });
  return { catalog, output_sha256: shaBuffer(Buffer.from(output)), output_bytes: Buffer.byteLength(output), application_reads: [sourcePath], network_reads: 0, child_processes: 0 };
}

function parseArgs(argv) {
  return new Map(argv.map((entry) => {
    const [key, ...rest] = entry.replace(/^--/, '').split('=');
    return [key, rest.length ? rest.join('=') : true];
  }));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const sourcePath = path.resolve(String(args.get('source') || FORMAL_SOURCE_PATH));
  const outputPath = path.resolve(String(args.get('output') || ''));
  if (!args.get('output')) fail(`usage: [--source=<${FORMAL_SOURCE_PATH}>] --output=<catalog.json>`);
  const result = buildFromPaths(sourcePath, outputPath);
  process.stdout.write(`${JSON.stringify({ schema_id: BUILDER_SCHEMA, source: sourcePath, output: outputPath, output_sha256: result.output_sha256, output_bytes: result.output_bytes, workflow_count: result.catalog.inventory.workflows, application_reads: 1, network_reads: 0, child_processes: 0 })}\n`);
}

if (import.meta.url === pathToFileURL(process.argv[1] || '').href) {
  main().catch((error) => {
    process.stderr.write(`${JSON.stringify({ schema_id: BUILDER_SCHEMA, error_code: error.code || 'R019_BUILD_FAILED', message: error.message })}\n`);
    process.exitCode = 1;
  });
}
