import * as THREE from "three";

// ============================================================
// HPSU-DAN Industrial PBR Material Library
// Enterprise-grade physically-based rendering materials
// ============================================================

/** Standard industrial metallic material (machined steel) */
export function createMetalMaterial(opts?: Partial<THREE.MeshStandardMaterialParameters>) {
  return new THREE.MeshStandardMaterial({
    color: 0x8797a6,
    metalness: 0.72,
    roughness: 0.3,
    envMapIntensity: 1.0,
    ...opts,
  });
}

/** Dark painted steel / cast iron (motor housing, bearing housings) */
export function createDarkMetalMaterial(opts?: Partial<THREE.MeshStandardMaterialParameters>) {
  return new THREE.MeshStandardMaterial({
    color: 0x172431,
    metalness: 0.55,
    roughness: 0.5,
    ...opts,
  });
}

/** Anodized aluminum accent parts */
export function createAccentMaterial(opts?: Partial<THREE.MeshStandardMaterialParameters>) {
  return new THREE.MeshStandardMaterial({
    color: 0x2a4f6a,
    metalness: 0.6,
    roughness: 0.35,
    ...opts,
  });
}

/** Polished shaft / bearing surface */
export function createPolishedMaterial(opts?: Partial<THREE.MeshStandardMaterialParameters>) {
  return new THREE.MeshStandardMaterial({
    color: 0x9aa7b4,
    metalness: 0.85,
    roughness: 0.15,
    ...opts,
  });
}

/** Transparent polycarbonate / acrylic guard */
export function createGuardMaterial(opts?: Partial<THREE.MeshPhysicalMaterialParameters>) {
  return new THREE.MeshPhysicalMaterial({
    color: 0x8fdfff,
    transparent: true,
    opacity: 0.16,
    roughness: 0.12,
    metalness: 0,
    transmission: 0.2,
    ...opts,
  });
}

/** Rubber / elastomer coupling elements */
export function createRubberMaterial(opts?: Partial<THREE.MeshStandardMaterialParameters>) {
  return new THREE.MeshStandardMaterial({
    color: 0x1a2d3c,
    metalness: 0.1,
    roughness: 0.85,
    ...opts,
  });
}

/** Copper winding / cable insulation */
export function createCopperMaterial(opts?: Partial<THREE.MeshStandardMaterialParameters>) {
  return new THREE.MeshStandardMaterial({
    color: 0xbf7534,
    metalness: 0.45,
    roughness: 0.4,
    ...opts,
  });
}

/** Fault state color palette */
export const FAULT_COLORS: Record<string, { color: number; emissive: number; label: string }> = {
  normal:             { color: 0x35d08b, emissive: 0x35d08b, label: "正常" },
  inner_race_fault:   { color: 0xff4868, emissive: 0xff4868, label: "内圈故障" },
  outer_race_fault:   { color: 0xff9b42, emissive: 0xff9b42, label: "外圈故障" },
  rolling_element_fault: { color: 0xa879ff, emissive: 0xa879ff, label: "滚动体故障" },
  compound_fault:     { color: 0xd46bff, emissive: 0xd46bff, label: "复合故障" },
  unknown:            { color: 0x6aa9ff, emissive: 0x6aa9ff, label: "待确认" },
};

/** Apply fault colors to a mesh material */
export function applyFaultMaterial(mesh: THREE.Mesh, faultKey: string, intensity = 0.5) {
  const palette = FAULT_COLORS[faultKey] || FAULT_COLORS.unknown;
  const mat = mesh.material as THREE.MeshStandardMaterial;
  mat.color.setHex(palette.color);
  mat.emissive.setHex(palette.emissive);
  mat.emissiveIntensity = intensity;
}

/** System paint scheme - color tokens for the whole platform */
export const COLORS = {
  background: "#081422",
  bgDark: "#06101b",
  gridPrimary: 0x245c7a,
  gridSecondary: 0x123044,
  highlight: 0x1ca8ff,
  accentCyan: 0x35d8ff,
  accentGreen: 0x35d08b,
  warning: 0xff9b42,
  danger: 0xff4868,
} as const;
