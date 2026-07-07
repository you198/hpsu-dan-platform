import { createI18n } from 'vue-i18n'

const messages = {
  'zh-CN': {
    common: { platform: '智能装备数字孪生与健康管理平台', logout: '退出', language: 'EN', adminOnly: '仅管理员可访问' },
    auth: { title: 'HPSU-DAN 智能诊断平台', subtitle: 'AI · 数字孪生 · 设备健康管理', username: '账号', password: '密码', login: '进入平台', hint: '演示账号由部署环境初始化，源码不保存密码。', failed: '账号或密码错误' },
    nav: { dashboard: '数字孪生驾驶舱', twin: '数字孪生设备', diagnosis: 'AI 智能诊断', analysis: '数据分析中心', system: '系统管理' },
    dashboard: { title: '设备全景态势', online: '设备在线', health: '综合健康度', speed: '当前转速', load: '轴承负载', channels: '采集通道', model: '诊断引擎', unregistered: '真实权重未注册', notice: '当前为平台联调数据，不代表论文模型诊断结论。' },
    twin: { title: 'SDUST 旋转机械实验台', hint: '左键旋转 · 滚轮缩放 · 右键平移', normal: '正常', inner: '内圈故障', outer: '外圈故障', rolling: '滚动体故障', compound: '复合故障', demo: '轻量程序化场景；GLB 资产接口待接入' },
    diagnosis: { title: 'AI 智能诊断', description: '生成一段联调振动信号，验证上传—推理—结果—孪生映射链路。', run: '运行联调诊断', running: '诊断中…', result: '诊断结果', confidence: '置信度', health: '健康度', history: '最近诊断任务', operator: '操作用户', warning: 'DEMO 引擎结果不可用于科研或维护决策', unavailable: '推理服务不可用，请先启动 8010 端口服务。' },
    analysis: { title: '数据分析中心', placeholder: '时域、FFT、CWT 与历史记录将在真实数据契约确认后接入。' },
    system: { title: '系统管理', role: '当前角色', database: '数据库', inference: '推理配置', assistant: '腾讯混元助手', enabled: '已启用', disabled: '未启用' },
  },
  'en-US': {
    common: { platform: 'Intelligent Equipment Digital Twin & Health Management', logout: 'Sign out', language: '中文', adminOnly: 'Administrator access only' },
    auth: { title: 'HPSU-DAN Diagnosis Platform', subtitle: 'AI · Digital Twin · Equipment Health', username: 'Username', password: 'Password', login: 'Enter platform', hint: 'Demo users are initialized from deployment settings; passwords are not stored in source.', failed: 'Invalid username or password' },
    nav: { dashboard: 'Digital Twin Cockpit', twin: 'Digital Twin Device', diagnosis: 'AI Diagnosis', analysis: 'Data Analysis', system: 'System Administration' },
    dashboard: { title: 'Equipment Overview', online: 'Device online', health: 'Health score', speed: 'Speed', load: 'Bearing load', channels: 'Channels', model: 'Diagnosis engine', unregistered: 'Real weights not registered', notice: 'Integration data only; this is not a research model conclusion.' },
    twin: { title: 'SDUST Rotating Machinery Test Bench', hint: 'Left drag to rotate · Wheel to zoom · Right drag to pan', normal: 'Normal', inner: 'Inner race fault', outer: 'Outer race fault', rolling: 'Rolling element fault', compound: 'Compound fault', demo: 'Lightweight procedural scene; GLB asset integration is pending' },
    diagnosis: { title: 'AI Diagnosis', description: 'Generate an integration signal to verify the upload, inference, result and twin mapping path.', run: 'Run integration diagnosis', running: 'Diagnosing…', result: 'Diagnosis result', confidence: 'Confidence', health: 'Health score', history: 'Recent diagnosis tasks', operator: 'Operator', warning: 'DEMO engine output must not be used for research or maintenance decisions', unavailable: 'Inference service is unavailable. Start the service on port 8010.' },
    analysis: { title: 'Data Analysis', placeholder: 'Time domain, FFT, CWT and history will follow after the real data contract is confirmed.' },
    system: { title: 'System Administration', role: 'Current role', database: 'Database', inference: 'Inference config', assistant: 'Tencent Hunyuan Assistant', enabled: 'Enabled', disabled: 'Disabled' },
  },
}

export const i18n = createI18n({ legacy: false, locale: localStorage.getItem('locale') || 'zh-CN', fallbackLocale: 'zh-CN', messages })
