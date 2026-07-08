# -*- coding: utf-8 -*-
import sys, os
cwd = os.getcwd()
target = os.path.join(cwd, 'hpsu-dan-platform', 'apps', 'web', 'src', 'api.ts')

content = """\
// ═══════════════════════════════════════════════════════
// HPSU-DAN Platform — API Client & Type Definitions
// 此文件是前后端之间的唯一接口契约
// 修改前请和 API 后端负责人确认 schema 变更
// ═══════════════════════════════════════════════════════

// ---------- Auth ----------
export interface LoginRequest {
  username: string
  password: string
}

export interface User {
  username: string
  role: 'admin' | 'guest'
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
}

// ---------- Dashboard ----------
export interface DeviceInfo {
  name: string
  status: 'online' | 'offline'
  health_score: number
  dataset: string
  task_id: string
  sample_length: number
  num_classes: number
}

export interface TelemetryInfo {
  speed_rpm: number
  load_n: number
  sampling_rate: number
  channels: number
}

export interface ModelInfo {
  id: string
  version: string
  registry_status: 'registered' | 'unregistered'
  runtime: string
  checkpoint: string
}

export interface ResearchSummary {
  best_accuracy: number
  total_experiments: number
  dataset_count: number
  method_count: number
  task_count: number
}

export interface DashboardSummary {
  device: DeviceInfo
  telemetry: TelemetryInfo
  model: ModelInfo
  research: ResearchSummary
  alerts: any[]
}

// ---------- Diagnosis ----------
export interface DiagnosisRequest {
  samples: number[]
  sampling_rate: number
  model_id: string
}

export interface WaveformPoint {
  x: number
  y: number
}

export interface SpectrumPoint {
  frequency: number
  magnitude: number
}

export interface EvidenceStatistics {
  mean: number
  variance: number
  rms: number
  peak: number
  kurtosis: number
  skewness: number
  crest_factor: number
}

export interface EvidenceWindow {
  window_index: number
  start: number
  length: number
}

export interface Evidence {
  waveform: WaveformPoint[]
  spectrum: SpectrumPoint[]
  markers: string[]
  statistics: EvidenceStatistics
  window: EvidenceWindow
}

export interface PredictionResult {
  label: string
  label_zh: string
  label_en: string
  confidence: number
  health_score: number
  twin_target: string
}

export interface TopKItem {
  label: string
  label_zh: string
  label_en: string
  probability: number
}

export interface InputSummary {
  sample_length: number
  sampling_rate: number
  channels: string[]
  normalization: string
}

export interface RuntimeInfo {
  preprocess_ms: number
  inference_ms: number
  postprocess_ms: number
  total_ms: number
  device: string
}

export interface DiagnosisResponse {
  task_id: string
  algorithm: string
  model_id: string
  model_version: string
  engine_mode: 'demo' | 'real' | 'completed_result'
  research_result: boolean
  input_summary: InputSummary
  evidence: Evidence
  prediction: PredictionResult
  topk: TopKItem[]
  runtime: RuntimeInfo
  notice: string
}

// ---------- Upload ----------
export interface QualityInfo {
  score: number
  length: number
  valid_length?: number
  missing_ratio: number
  outlier_ratio: number
  window_length: number
  sampling_rate: number
  has_required_window: boolean
}

export interface TaskView {
  task_id: string
  task_type: string
  status: string
  created_by: string
  model_id: string | null
  model_version: string | null
  input_file_id: string | null
  result_id: string | null
  error_code: string | null
  error_message_key: string | null
  created_at: string
  started_at: string | null
  finished_at: string | null
}

export interface UploadDiagnosisResponse {
  task: TaskView
  result: DiagnosisResponse | null
  quality: QualityInfo | null
}

// ---------- Diagnosis History ----------
export interface DiagnosisHistoryItem {
  task_id: string
  requested_by: string
  model_id: string
  engine_mode: string
  label: string
  confidence: number
  created_at: string
}

// ---------- Task Detail ----------
export interface UploadedFileView {
  file_id: string
  original_name: string
  status: string
  size_bytes: number
  uploaded_by: string
  error_code: string | null
  quality: QualityInfo | null
  created_at: string
}

export interface TaskDetail extends TaskView {
  input_file?: UploadedFileView | null
  result?: DiagnosisResponse | null
}

// ---------- Compute ----------
export interface QueueStatus {
  cpu_default_queue: { status: string }
  gpu_inference_queue: { status: string }
  gpu_training_queue: { status: string }
  gpu_analysis_queue: { status: string }
  report_queue: { status: string }
}

export interface ComputeStatus {
  compute_default_device: string
  gpu_enabled: boolean
  gpu_available: boolean
  gpu_visible_devices: string
  gpu_max_memory_mb: number
  cpu_fallback_enabled: boolean
  batch_inference_max_windows: number
  queues: QueueStatus
  nvidia_smi_available: boolean
}

// ---------- Research ----------
export interface ResearchResultItem {
  result_id: string
  title: string
  visibility: 'public' | 'private'
  dataset: string
  task_id: string
  method: string
  implementation: string
  run_id: string
  model_id: string
  model_version: string
  status: string
  source: string
  metrics: Record<string, number>
  assets: Record<string, string>
  checkpoint?: string
  checkpoint_exists?: boolean
}

export interface ResearchOptions {
  datasets: Record<string, any>
  transfer_tasks: Record<string, any>
  methods: Record<string, any>
  results: ResearchResultItem[]
  summary: {
    result_count: number
    datasets: Record<string, number>
    methods: Record<string, number>
    sources: Record<string, number>
    tasks: Record<string, number>
    cache_created_at: number
    cache_ttl_seconds: number
  }
}

// ---------- System ----------
export interface SystemStatus {
  environment: string
  database: string
  inference_url_configured: boolean
  assistant_enabled: boolean
}

// ---------- Assistant ----------
export interface AssistantMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
}

export interface AssistantChatRequest {
  messages: AssistantMessage[]
  temperature: number
  max_tokens: number
}

export interface AssistantReply {
  model: string
  content: string
}

// ═══════════════════════════════════════════════════════
// API Client
// ═══════════════════════════════════════════════════════

function token() {
  return localStorage.getItem('access_token') || ''
}

export async function api(path, options = {}) {
  const headers = new Headers(options.headers)
  if (!(options.body instanceof FormData)) headers.set('Content-Type', 'application/json')
  if (token()) headers.set('Authorization', 'Bearer ' + token())
  const response = await fetch('/api/v1' + path, { ...options, headers })
  if (!response.ok) throw new Error((await response.json().catch(() => ({}))).detail || 'HTTP_' + response.status)
  return response.json()
}

// ---------- Auth ----------
export function login(data) {
  return api('/auth/login', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function getMe() {
  return api('/auth/me')
}

// ---------- Dashboard ----------
export function getDashboardSummary() {
  return api('/dashboard/summary')
}

// ---------- Diagnosis ----------
export function predictDiagnosis(data) {
  return api('/diagnosis/predict', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export function uploadDiagnosis(file, samplingRate, modelId) {
  const form = new FormData()
  form.append('file', file)
  if (samplingRate !== undefined) form.append('sampling_rate', String(samplingRate))
  if (modelId !== undefined) form.append('model_id', modelId)
  return api('/diagnosis/upload', {
    method: 'POST',
    body: form,
  })
}

export function getDiagnosisHistory(limit) {
  if (limit === undefined) limit = 20
  return api('/diagnosis/history?limit=' + limit)
}

export function getDiagnosisDetail(taskId) {
  return api('/diagnosis/' + taskId)
}

// ---------- Tasks ----------
export function getTaskHistory(limit) {
  if (limit === undefined) limit = 20
  return api('/tasks?limit=' + limit)
}

export function getTaskDetail(taskId) {
  return api('/tasks/' + taskId)
}

export function rerunTask(taskId) {
  return api('/tasks/' + taskId + '/rerun', { method: 'POST' })
}

// ---------- Files ----------
export function getQuarantinedFiles(limit) {
  if (limit === undefined) limit = 20
  return api('/files/quarantine?limit=' + limit)
}

// ---------- Compute ----------
export function getComputeStatus() {
  return api('/compute/status')
}

// ---------- Research ----------
export function getResearchOptions() {
  return api('/research/options')
}

export function refreshResearchRegistry() {
  return api('/research/refresh', { method: 'POST' })
}

export function getResearchResult(resultId) {
  return api('/research/results/' + resultId)
}

// ---------- System ----------
export function getSystemStatus() {
  return api('/system/status')
}

// ---------- Assistant ----------
export function chatWithAssistant(content) {
  return api('/assistant/chat', {
    method: 'POST',
    body: JSON.stringify({
      messages: [{ role: 'user', content }],
      temperature: 0.2,
      max_tokens: 1200,
    }),
  })
}
"""

open(target, 'w', encoding='utf-8').write(content)
print("api.ts written OK: " + str(len(content)) + " bytes")
