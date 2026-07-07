import { defineStore } from 'pinia';
function inferFaultFamily(prediction) {
    const target = prediction.twin_target || '';
    const code = (prediction.code || prediction.label || '').toUpperCase();
    if (target.includes('inner'))
        return 'inner_race_fault';
    if (target.includes('outer'))
        return 'outer_race_fault';
    if (target.includes('rolling'))
        return 'rolling_element_fault';
    if (target.includes('compound'))
        return 'compound_fault';
    if (code === 'K001' || code === 'NC' || code === 'NORMAL')
        return 'normal';
    if (code.startsWith('KI'))
        return 'inner_race_fault';
    if (code.startsWith('KA'))
        return 'outer_race_fault';
    if (code.startsWith('KB'))
        return 'rolling_element_fault';
    return 'unknown';
}
function evidenceFor(faultKey) {
    const table = {
        normal: {
            waveformMode: 'stable',
            spectrumMarkers: ['1X'],
            suggestionZh: '设备运行平稳，建议保持当前巡检周期。',
            suggestionEn: 'The equipment is stable. Keep the current inspection interval.',
        },
        inner_race_fault: {
            waveformMode: 'impact_periodic',
            spectrumMarkers: ['BPFI', '2xBPFI'],
            suggestionZh: '疑似轴承内圈冲击故障，建议检查内圈滚道、装配间隙和润滑状态。',
            suggestionEn: 'Possible inner race impact fault. Inspect the raceway, clearance and lubrication.',
        },
        outer_race_fault: {
            waveformMode: 'impact_fixed',
            spectrumMarkers: ['BPFO', '2xBPFO'],
            suggestionZh: '疑似轴承外圈固定缺陷，建议检查外圈承载区、轴承座紧固和润滑状态。',
            suggestionEn: 'Possible outer race defect. Inspect the loaded zone, housing fastening and lubrication.',
        },
        rolling_element_fault: {
            waveformMode: 'impact_modulated',
            spectrumMarkers: ['BSF', 'FTF'],
            suggestionZh: '疑似滚动体或复合冲击故障，建议检查滚珠表面、保持架和轴承污染情况。',
            suggestionEn: 'Possible rolling element or compound impact fault. Inspect balls, cage and contamination.',
        },
        compound_fault: {
            waveformMode: 'compound',
            spectrumMarkers: ['BPFI', 'BPFO', 'BSF'],
            suggestionZh: '疑似多部位复合故障，建议停机检查轴承组件并复测振动信号。',
            suggestionEn: 'Possible compound fault. Stop the machine, inspect the bearing assembly and retest vibration.',
        },
        unknown: {
            waveformMode: 'compound',
            spectrumMarkers: ['BPFI', 'BPFO', 'BSF'],
            suggestionZh: '模型置信或类别映射需要复核，建议结合原始信号和工况重新确认。',
            suggestionEn: 'The model confidence or class mapping needs review. Recheck the signal and operating condition.',
        },
    };
    return table[faultKey];
}
export const useDiagnosisStore = defineStore('diagnosis', {
    state: () => ({
        current: {
            faultKey: 'normal',
            code: 'K001',
            labelZh: '正常基准 K001',
            labelEn: 'Normal K001',
            confidence: 0.92,
            healthScore: 92,
            riskLevel: 'normal',
            twinTarget: 'bearing',
            waveformMode: 'stable',
            spectrumMarkers: ['1X'],
            suggestionZh: '设备运行平稳，建议保持当前巡检周期。',
            suggestionEn: 'The equipment is stable. Keep the current inspection interval.',
            engineMode: 'demo',
            modelVersion: 'unregistered',
            waveformPoints: [],
            spectrumPoints: [],
            updatedAt: new Date().toISOString(),
            rawResult: null,
        },
    }),
    actions: {
        applyResult(result) {
            const prediction = (result?.prediction || {});
            const faultKey = inferFaultFamily(prediction);
            const evidence = evidenceFor(faultKey);
            this.current = {
                faultKey,
                code: prediction.code || prediction.label || faultKey,
                labelZh: prediction.label_zh || prediction.label || faultKey,
                labelEn: prediction.label_en || prediction.label || faultKey,
                confidence: Number(prediction.confidence || 0),
                healthScore: Number(prediction.health_score || 0),
                riskLevel: prediction.risk_level || (faultKey === 'normal' ? 'normal' : 'severe'),
                twinTarget: prediction.twin_target || 'bearing',
                waveformMode: evidence.waveformMode,
                spectrumMarkers: [...(result?.evidence?.markers || evidence.spectrumMarkers)],
                waveformPoints: Array.isArray(result?.evidence?.waveform) ? result.evidence.waveform : [],
                spectrumPoints: Array.isArray(result?.evidence?.spectrum) ? result.evidence.spectrum : [],
                suggestionZh: evidence.suggestionZh,
                suggestionEn: evidence.suggestionEn,
                engineMode: result?.engine_mode || 'demo',
                modelVersion: result?.model_version || 'unregistered',
                updatedAt: new Date().toISOString(),
                rawResult: result,
            };
        },
        setFault(faultKey) {
            const evidence = evidenceFor(faultKey);
            const labels = {
                normal: ['K001', '正常基准 K001', 'Normal K001', 'bearing'],
                inner_race_fault: ['KI16', '内圈故障 KI16', 'Inner race fault KI16', 'bearing.inner_race'],
                outer_race_fault: ['KA16', '外圈故障 KA16', 'Outer race fault KA16', 'bearing.outer_race'],
                rolling_element_fault: ['KB23', '滚动体故障 KB23', 'Rolling element fault KB23', 'bearing.rolling_element'],
                compound_fault: ['KB27', '复合故障 KB27', 'Compound fault KB27', 'bearing.rolling_element'],
                unknown: ['UNK', '待确认故障', 'Unknown fault', 'bearing.unknown'],
            };
            const [code, labelZh, labelEn, twinTarget] = labels[faultKey];
            this.current = {
                ...this.current,
                faultKey,
                code,
                labelZh,
                labelEn,
                confidence: faultKey === 'normal' ? 0.92 : 0.84,
                healthScore: faultKey === 'normal' ? 92 : 42,
                riskLevel: faultKey === 'normal' ? 'normal' : 'severe',
                twinTarget,
                waveformMode: evidence.waveformMode,
                spectrumMarkers: [...evidence.spectrumMarkers],
                waveformPoints: [],
                spectrumPoints: [],
                suggestionZh: evidence.suggestionZh,
                suggestionEn: evidence.suggestionEn,
                updatedAt: new Date().toISOString(),
            };
        },
    },
});
