# Penjaga Keraton: Nusantara Tower Defense

## Gambaran Umum
Game 3D tower defense bertema Nusantara–horor ringan. Pemain sebagai Penjaga Keraton yang menggunakan pusaka dan penjaga gaib untuk menghentikan serangan hantu sebelum mencapai inti keraton.

## Alur Game
- Masuk ke `Lobby Keraton` (pendopo) berisi:
  - Galeri Hantu (5 musuh) dan Galeri Defense/Pusaka (5 tower)
  - NPC `Juru Kunci`: interaksi menampilkan GUI lore & cara bermain
  - Portal/Gerbang menuju `Arena`
- Di `Arena`:
  - Lihat jalur musuh (path) dan node penempatan tower
  - Tempatkan/upgrade tower, kalahkan wave hantu untuk mendapat uang
  - Jika base hancur → `Game Over` (kembali ke lobby). Jika semua wave selesai → `Menang`

## Aset Utama (10)
### Musuh (5)
1. **Pocong** — Basic: HP rendah, speed normal
2. **Pocong Merah** — Fast: lebih cepat, HP sedang
3. **Kuntilanak** — Ranged/Special: serangan jarak jauh, bisa punya shield kabut
4. **Genderuwo** — Tank: sangat lambat, HP sangat tinggi
5. **Tuyul** — Sneaky/Runner: sangat cepat, HP sangat rendah, jika lolos kurangi uang

### Tower/Pusaka (5)
6. **Keris Terbang** — Single-target DPS: attack speed tinggi
7. **Tombak Keraton** — Piercing: proyektil/beam menembus beberapa musuh
8. **Obor Penjaga** — AoE/DoT: membakar area, damage per detik
9. **Gamelan Spirit** — Support/Slow: aura memperlambat + sedikit damage
10. **Payung Keraton** — Buff/Shield: shield ke tower sekitar atau kurangi damage ke base

## Sistem Bersama
- Lobby/Pendopo, Portal/Teleport, NPC + GUI
- Arena/Map TD (path & node penempatan)
- Sistem Wave, Ekonomi (uang), Base Health, Win/Lose

## MVP (Milestone 1)
- 1 `LobbyScene`, 1 `ArenaScene` (jalur tunggal, 6–8 node)
- Musuh: Pocong, Pocong Merah, Genderuwo
- Tower: Keris Terbang, Tombak Keraton, Obor Penjaga
- Fitur: follow path, placement, targeting, proyektil, AoE, wave spawner, base HP, currency, upgrade level 1
- Milestone 2: tambah Kuntilanak, Tuyul, Gamelan, Payung + polish galeri

## Spesifikasi Teknis (Singkat)
- `Enemy`: HP, speed, reward, baseDamage, tag; state: spawn→move→hit/die; follow waypoint
- `Tower`: range, attackRate, biaya, upgrade; targeting: nearest/first/strongest; snap ke node
- `Keris`: proyektil single-target cepat
- `Tombak`: serangan lurus dengan `maxPierce`
- `Obor`: aura DoT radius, tick period
- `Gamelan`: aura slow (%), radius, pulse damage
- `Payung`: aura shield (HP tambahan / damage reduction) atau reduksi damage ke base
- `Kuntilanak`: proyektil jarak jauh + opsi shield kabut singkat
- `Tuyul`: speed sangat tinggi, efek pengurangan uang saat mencapai base

## Sistem Gameplay
- `WaveManager`: konfigurasi wave (tipe/jumlah/rate), jeda antar wave, scaling
- `PathSystem`: daftar waypoint, arah gerak
- `Placement`: node valid, biaya, opsi jual (opsional)
- `Combat`: proyektil (damage, speed, pierce), AoE (tick), Aura (apply/remove)
- `Economy`: uang per kill, biaya & kurva upgrade, UI
- `BaseHealth`: HP, damage saat musuh lolos, kondisi game over
- `UI`: HUD HP, uang, info wave; popup tutorial di lobby

## Struktur Proyek (Usulan Unity)
```
Assets/
  Art/
    Enemies/
    Towers/
  Prefabs/
  Materials/
  Scripts/
    Enemies/
    Towers/
    Systems/
  UI/
Scenes/
  LobbyScene.unity
  ArenaScene.unity
```
Namespace skrip: `KeratonTD.*`

## Pembagian Tugas
- **Mahasiswa A**: Pocong, Pocong Merah, Genderuwo, Keris Terbang, Tombak Keraton
- **Mahasiswa B**: Kuntilanak, Tuyul, Obor Penjaga, Gamelan Spirit, Payung Keraton
Untuk tiap aset: model placeholder ok → prefab → skrip perilaku → stat dasar → hook VFX/SFX

## Risiko & Mitigasi
- Waktu modeling 3D: mulai dari blockout/placeholders, refine di akhir
- Balancing kompleks: stat sederhana dulu, tambah kurva setelah core fun
- Performa aura/stack: batasi tumpukan, cache target per tick
- Scope polish: utamakan gameplay, galeri dipoles setelah loop stabil

## Langkah Berikutnya
1. Pilih engine (disarankan Unity)
2. Buat project & folder sesuai struktur
3. Buat prefab placeholder untuk 3 musuh + 3 tower MVP
4. Implementasi sistem: Path, Wave, Base, Placement, Combat
5. Tambah UI minimal & portal lobby

## Workflow Blender → Roblox Studio
- Kode aset Blender ada di folder `bpy-scripts/`:
  - `kuntilanak.py`, `tuyul.py`, `obor_penjaga.py`, `gamelan_spirit.py`, `payung_keraton.py`, dan utilitas `common_utils.py`
- Cara menjalankan di Blender:
  - Buka Blender → `Scripting` tab → `Text Editor` → buka file skrip → `Run Script`
  - Opsional: isi parameter ekspor FBX di fungsi `main(filepath_fbx=...)`
- Ekspor ke FBX:
  - Dari UI: `File > Export > FBX` (nonaktifkan `Add Leaf Bones`, aktifkan `Apply Transform`)
  - Atau gunakan helper `export_fbx()` di `common_utils.py`
- Import ke Roblox Studio:
  - `Asset Manager > Bulk Import` atau `Import 3D` → pilih file `.fbx`
  - Set `Collision` dan `Anchored` sesuai kebutuhan tower/enemy
  - Buat `Model` dan atur pivot/root sesuai empty `*Root` yang dibuat skrip

Catatan: `bpy` dan `mathutils` hanya tersedia di Python internal Blender. Jalankan skrip langsung di Blender.
