# Phase 0 Frontend Audit

Date: 2026-07-10

## Stack

- Framework: Vue `3.5.16`
- Language: TypeScript `5.8.x`
- Build tool: Vite `6.4.x` runtime output, package range `^6.3.5`
- Router: Vue Router `4.5.1`
- State: Pinia `3.0.3`
- Charts: ECharts `5.6.0`
- 3D library installed: Three.js `0.177.0`
- TresJS/Babylon.js: not installed

## Scripts

- `npm run typecheck`: configured and passing.
- `npm run build`: configured and passing.
- `npm run lint`: not configured.
- `npm run test`: not configured.

## Important Pages

- `src/views/AppShell.vue`: shell and navigation host.
- `src/views/DashboardCompetitionView.vue`: competition dashboard, currently driven by mock/static twin state.
- `src/views/DigitalTwinCompetitionView.vue`: dataset-aware twin page, currently uses SVG/component testbench.
- `src/views/DiagnosisView.vue`: upload/predict UI, calls diagnosis API but store still maps legacy `prediction/evidence`.
- `src/views/ResearchWorkbenchView.vue`: calls research APIs and has frontend fallback data.
- `src/views/SystemView.vue`: calls `/system/status`, has fallback status if the API call fails.
- `src/views/LoginView.vue`: JWT login/demo login flow.

## Digital Twin Current Mode

Current formal rendering path is still component/SVG-oriented:

- `DatasetAwareTestBench.vue`
- `PuTestBench.vue`
- `SdustTestBench.vue`
- `FlatTwinDiagram.vue`

Three.js support code exists under `src/three`, including scene manager, rig parts, materials, picking, camera tour, model loader, and fault highlighter. The default competition pages still use `DatasetAwareTestBench`, not a full WebGL scene.

## Static And Mock Data

Mock/static frontend sources still used:

- `src/mocks/twinMock.ts`
- `src/mocks/researchMock.ts`
- `src/mocks/experimentsMock.ts`
- `src/config/twinProfiles.ts`
- `src/config/faultTargetMap.ts`
- `src/config/datasetConditions.ts`

This is acceptable for Phase 0 but must be replaced or clearly labeled in Phase 5.

## API Client Layer

Frontend services exist:

- `src/services/apiClient.ts`
- `src/services/authApi.ts`
- `src/services/diagnosisApi.ts`
- `src/services/researchApi.ts`
- `src/services/experimentsApi.ts`
- `src/services/systemApi.ts`
- `src/services/taskApi.ts`
- `src/services/assistantApi.ts`

`VITE_API_BASE_URL` is supported through `API_BASE`. Current code also reads `VITE_USE_MOCK`; the prompt prefers `VITE_ENABLE_MOCK`, so this should be aligned in a later phase.

## Assets

Frontend public assets currently contain placeholder documentation:

- `public/assets/models/README.txt`
- `public/assets/testbench/README.md`

No GLB/GLTF/OBJ/FBX/STL/STEP/Blend assets were found in the platform or workspace scan.

## Test Results

- `npm run typecheck`: passed.
- `npm run build`: passed.
- Build warning: main JS chunk is larger than 500 kB.
- `npm run lint`: missing script.
- `npm run test`: missing script.

## Key Risks

- Dashboard and Digital Twin still depend on mock/static state.
- Diagnosis store should consume `diagnosisResult` as the primary DTO.
- No true 3D/CAD assets exist yet; Three.js phase needs programmatic geometry or external modeling assets.
- Current UI still contains strong glow/glass styling in several places; prompt asks to reduce non-essential glow later.
