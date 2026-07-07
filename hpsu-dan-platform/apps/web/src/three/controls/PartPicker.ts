import * as THREE from "three";

// ============================================================
// PartPicker - Mouse-driven 3D part interaction system
// Raycasting for hover highlighting and click event emission
// ============================================================

export interface PartInfo {
  name: string;
  labelZh: string;
  labelEn: string;
  specs?: string;
}

export const PART_LIBRARY: Record<string, PartInfo> = {
  motor:             { name: "motor", labelZh: "驱动电机", labelEn: "Drive Motor", specs: "2200W, 0-3000 rpm" },
  coupling:          { name: "coupling", labelZh: "弹性联轴器", labelEn: "Elastic Coupling", specs: "45 steel, 50mm OD" },
  shaft:             { name: "shaft", labelZh: "传动转轴", labelEn: "Drive Shaft", specs: "40Cr, 20mm dia" },
  bearing_6205:      { name: "bearing_6205", labelZh: "测试轴承 6205", labelEn: "Test Bearing 6205", specs: "ID25 OD52, 9 balls" },
  bearing_outer_race:{ name: "bearing_outer_race", labelZh: "轴承外圈", labelEn: "Outer Race", specs: "52mm OD" },
  bearing_inner_race:{ name: "bearing_inner_race", labelZh: "轴承内圈", labelEn: "Inner Race", specs: "25mm ID" },
  gearbox:           { name: "gearbox", labelZh: "行星齿轮箱", labelEn: "Planetary Gearbox", specs: "Ratio 4:1, 3 planets" },
  load_disk:         { name: "load_disk", labelZh: "负载盘/制动器", labelEn: "Load Disk / Brake" },
  sensor_x:          { name: "sensor_x", labelZh: "X向振动传感器", labelEn: "X-Axis Sensor", specs: "25.6kHz, 100mV/g" },
  sensor_y:          { name: "sensor_y", labelZh: "Y向振动传感器", labelEn: "Y-Axis Sensor", specs: "25.6kHz, 100mV/g" },
  sensor_z:          { name: "sensor_z", labelZh: "Z向振动传感器", labelEn: "Z-Axis Sensor", specs: "25.6kHz, 100mV/g" },
  speed_controller:  { name: "speed_controller", labelZh: "转速控制器", labelEn: "Speed Controller" },
};

export class PartPicker {
  private raycaster = new THREE.Raycaster();
  private mouse = new THREE.Vector2();
  private hovered: THREE.Object3D | null = null;
  private interactables: THREE.Object3D[] = [];
  private container: HTMLElement;
  private camera: THREE.Camera;

  public onHover?: (name: string | null) => void;
  public onClick?: (name: string) => void;

  constructor(container: HTMLElement, camera: THREE.Camera) {
    this.container = container;
    this.camera = camera;
    this.setupListeners();
  }

  /** Register parts for raycasting */
  register(...objects: THREE.Object3D[]) {
    this.interactables.push(...objects);
  }

  /** Clear registered parts */
  clear() {
    this.interactables.length = 0;
  }

  private setupListeners() {
    this.container.addEventListener("pointermove", (e) => this.onPointerMove(e));
    this.container.addEventListener("click", (e) => this.onClickEvent(e));
  }

  dispose() {
    // Listeners cleanup is handled by the DOM
  }

  private findPartName(obj: THREE.Object3D): string | null {
    let current: THREE.Object3D | null = obj;
    while (current) {
      if (current.userData?.partName) {
        return current.userData.partName;
      }
      current = current.parent;
    }
    return null;
  }

  private onPointerMove(event: PointerEvent) {
    const rect = this.container.getBoundingClientRect();
    this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    this.raycaster.setFromCamera(this.mouse, this.camera);
    const intersects = this.raycaster.intersectObjects(this.interactables, true);

    // Restore previous highlight
    if (this.hovered) {
      const mat = (this.hovered as THREE.Mesh).material as THREE.MeshStandardMaterial;
      if (mat && mat.emissive) {
        mat.emissiveIntensity = Math.max(0.02, mat.emissiveIntensity - 0.8);
      }
      this.hovered = null;
      this.container.style.cursor = "grab";
      this.onHover?.(null);
    }

    // Apply new highlight
    if (intersects.length > 0) {
      const obj = intersects[0].object;
      const name = this.findPartName(obj);
      if (!name) return;

      this.hovered = obj;
      const mat = (obj as THREE.Mesh).material as THREE.MeshStandardMaterial;
      if (mat && mat.emissive) {
        mat.emissiveIntensity = Math.min(1.5, mat.emissiveIntensity + 0.8);
      }
      this.container.style.cursor = "pointer";
      this.onHover?.(name);
    }
  }

  private onClickEvent(event: PointerEvent) {
    const rect = this.container.getBoundingClientRect();
    this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    this.raycaster.setFromCamera(this.mouse, this.camera);
    const intersects = this.raycaster.intersectObjects(this.interactables, true);

    if (intersects.length > 0) {
      const name = this.findPartName(intersects[0].object);
      if (name) {
        this.onClick?.(name);
      }
    }
  }
}
