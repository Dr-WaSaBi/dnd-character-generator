import json
import os
import traceback

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QScrollArea, QFileDialog, QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence

from ui.editors import (
    AbilityScoreEditor, CharacterInfoEditor, SavingThrowEditor,
    SkillsEditor, CombatStatsEditor, AttacksSpellsEditor,
    EquipmentEditor, PersonalityEditor, FeaturesEditor, ProficienciesEditor,
    StartingEquipmentDialog,
)
from ui.styles import COLOR_WINDOW_BG, FONT_BODY, SHEET_STYLE
from ui.sheet_view import SheetView


class CharacterSheetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D&D 5e Character Generator")
        self.setMinimumSize(1050, 720)
        self.resize(1280, 900)
        self.setStyleSheet(SHEET_STYLE)
        self._char_data: dict = {}
        self._current_file: str | None = None
        self._dirty: bool = False
        self._build_ui()
        self._build_menu()

    def _build_ui(self):
        outer = QWidget()
        outer.setStyleSheet(f"background-color: {COLOR_WINDOW_BG};")
        self.setCentralWidget(outer)
        outer_lo = QVBoxLayout(outer)
        outer_lo.setContentsMargins(12, 12, 12, 12)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        outer_lo.addWidget(scroll)

        self._sheet_view = SheetView()
        self._sheet_view.section_clicked.connect(self._on_section_clicked)
        scroll.setWidget(self._sheet_view)

        self.statusBar().setFixedHeight(26)
        self.statusBar().showMessage(
            "  Click any section to begin building your character."
        )

    # ── Menu bar ─────────────────────────────────────────────────────────────

    def _build_menu(self):
        mb = self.menuBar()
        mb.setStyleSheet(
            f"QMenuBar{{background:{COLOR_WINDOW_BG};color:#D4AF37;"
            f"font-family:{FONT_BODY};font-size:9pt;padding:2px;}}"
            f"QMenuBar::item:selected{{background:#3A1A0A;}}"
            f"QMenu{{background:{COLOR_WINDOW_BG};color:#D4AF37;"
            f"font-family:{FONT_BODY};font-size:9pt;border:1px solid #D4AF37;}}"
            f"QMenu::item:selected{{background:#3A1A0A;}}"
        )
        file_menu = mb.addMenu("File")

        act_new = QAction("New Character", self)
        act_new.setShortcut(QKeySequence.StandardKey.New)
        act_new.triggered.connect(self._on_new)
        file_menu.addAction(act_new)

        file_menu.addSeparator()

        act_open = QAction("Open Character…", self)
        act_open.setShortcut(QKeySequence.StandardKey.Open)
        act_open.triggered.connect(self._on_open)
        file_menu.addAction(act_open)

        file_menu.addSeparator()

        act_save = QAction("Save", self)
        act_save.setShortcut(QKeySequence.StandardKey.Save)
        act_save.triggered.connect(self._on_save)
        file_menu.addAction(act_save)

        act_save_as = QAction("Save As…", self)
        act_save_as.setShortcut(QKeySequence.StandardKey.SaveAs)
        act_save_as.triggered.connect(self._on_save_as)
        file_menu.addAction(act_save_as)

        file_menu.addSeparator()

        act_starting = QAction("Apply Starting Equipment…", self)
        act_starting.triggered.connect(self._on_starting_equipment)
        file_menu.addAction(act_starting)

        act_pdf = QAction("Export PDF…", self)
        act_pdf.setShortcut(QKeySequence("Ctrl+P"))
        act_pdf.triggered.connect(self._on_export_pdf)
        file_menu.addAction(act_pdf)

        file_menu.addSeparator()

        act_quit = QAction("Quit", self)
        act_quit.setShortcut(QKeySequence("Ctrl+Q"))
        act_quit.triggered.connect(self.close)
        file_menu.addAction(act_quit)

    # ── File I/O ──────────────────────────────────────────────────────────────

    def _on_new(self):
        if self._dirty and not self._confirm_discard():
            return
        self._char_data = {}
        self._current_file = None
        self._dirty = False
        self._reset_sheet()
        self.setWindowTitle("D&D 5e Character Generator")
        self.statusBar().showMessage("  New character — select a section to begin.")

    def _on_starting_equipment(self):
        dlg = StartingEquipmentDialog(char_data=self._char_data, parent=self)
        dlg.equipment_chosen.connect(self._apply_starting_equipment)
        dlg.exec()

    def _apply_starting_equipment(self, items: list, gold_gp: int):
        equip = self._char_data.setdefault("equipment", {"items": [], "currency": {}})
        equip.setdefault("items", [])
        equip.setdefault("currency", {"CP": 0, "SP": 0, "EP": 0, "GP": 0, "PP": 0})
        equip["items"].extend(items)
        equip["currency"]["GP"] = equip["currency"].get("GP", 0) + gold_gp
        self._on_equipment_saved(equip)
        self._dirty = True
        self.statusBar().showMessage(
            f"  ✔  Starting equipment applied — {len(items)} items, {gold_gp} gp added."
        )

    def _on_open(self):
        if self._dirty and not self._confirm_discard():
            return
        path, _ = QFileDialog.getOpenFileName(
            self, "Open Character", "",
            "D&D Character (*.dnd5e);;JSON Files (*.json);;All Files (*)"
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._char_data = data
            self._current_file = path
            self._dirty = False
            self._apply_loaded_data()
            self.setWindowTitle(f"D&D 5e — {os.path.basename(path)}")
            self.statusBar().showMessage(f"  Opened: {os.path.basename(path)}")
        except Exception as exc:
            QMessageBox.critical(
                self, "Open failed",
                f"{type(exc).__name__}: {exc}\n\n{traceback.format_exc()}"
            )

    def _on_save(self):
        if self._current_file:
            self._write_file(self._current_file)
        else:
            self._on_save_as()

    def _on_save_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Character", "",
            "D&D Character (*.dnd5e);;JSON Files (*.json);;All Files (*)"
        )
        if not path:
            return
        if not path.endswith((".dnd5e", ".json")):
            path += ".dnd5e"
        self._current_file = path
        self._write_file(path)
        self.setWindowTitle(f"D&D 5e — {os.path.basename(path)}")

    def _write_file(self, path: str):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self._char_data, f, indent=2)
            self._dirty = False
            self.statusBar().showMessage(f"  ✔  Saved: {os.path.basename(path)}")
        except Exception as exc:
            QMessageBox.critical(self, "Save failed", str(exc))

    def _on_export_pdf(self):
        name = self._char_data.get("character_info", {}).get("character_name", "character") or "character"
        default = name.replace(" ", "_") + ".pdf"
        path, _ = QFileDialog.getSaveFileName(
            self, "Export PDF", default,
            "PDF Files (*.pdf);;All Files (*)"
        )
        if not path:
            return
        if not path.endswith(".pdf"):
            path += ".pdf"
        try:
            from ui.pdf_export import export_pdf
            export_pdf(self._char_data, path)
            self.statusBar().showMessage(f"  ✔  PDF exported: {os.path.basename(path)}")
            QMessageBox.information(self, "PDF Exported",
                f"Character sheet saved to:\n{path}")
        except Exception as exc:
            QMessageBox.critical(self, "PDF Export Failed",
                f"{type(exc).__name__}: {exc}\n\n{traceback.format_exc()}")

    def _confirm_discard(self) -> bool:
        reply = QMessageBox.question(
            self, "Unsaved changes",
            "You have unsaved changes. Save before continuing?",
            QMessageBox.StandardButton.Save |
            QMessageBox.StandardButton.Discard |
            QMessageBox.StandardButton.Cancel,
        )
        if reply == QMessageBox.StandardButton.Save:
            self._on_save()
            return True
        return reply == QMessageBox.StandardButton.Discard

    def closeEvent(self, event):
        if self._dirty and not self._confirm_discard():
            event.ignore()
        else:
            event.accept()

    def _reset_sheet(self):
        self._sheet_view.refresh({})

    def _apply_loaded_data(self):
        self._sheet_view.refresh(self._char_data)
        self._dirty = False

    def _on_section_clicked(self, number: int):
        if number == 1:
            self._open_info_editor()
            return
        if number == 2:
            self._open_ability_editor()
            return
        if number == 3:
            self._open_saving_throws_editor()
            return
        if number == 4:
            self._open_skills_editor()
            return
        if number == 5:
            self._open_combat_stats_editor()
            return
        if number == 6:
            self._open_attacks_spells_editor()
            return
        if number == 7:
            self._open_equipment_editor()
            return
        if number == 8:
            self._open_personality_editor()
            return
        if number == 9:
            self._open_features_editor()
            return
        if number == 10:
            self._open_proficiencies_editor()
            return
        self.statusBar().showMessage(
            f"  ▶  Section {number} — editor coming soon"
        )

    def _open_info_editor(self):
        dlg = CharacterInfoEditor(
            existing=self._char_data.get("character_info"),
            parent=self,
        )
        dlg.info_saved.connect(self._on_info_saved)
        dlg.exec()

    def _on_info_saved(self, info: dict):
        self._char_data["character_info"] = info
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Character info saved.")

    def _open_saving_throws_editor(self):
        dlg = SavingThrowEditor(
            char_data=self._char_data,
            existing=self._char_data.get("saving_throws"),
            parent=self,
        )
        dlg.throws_saved.connect(self._on_throws_saved)
        dlg.exec()

    def _on_throws_saved(self, throws: dict):
        self._char_data["saving_throws"] = throws
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Saving throws saved.")

    def _open_personality_editor(self):
        dlg = PersonalityEditor(
            existing=self._char_data.get("personality"),
            parent=self,
        )
        dlg.data_saved.connect(self._on_personality_saved)
        dlg.exec()

    def _on_personality_saved(self, data: dict):
        self._char_data["personality"] = data
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Personality saved.")

    def _open_features_editor(self):
        dlg = FeaturesEditor(
            char_data=self._char_data,
            existing=self._char_data.get("features"),
            parent=self,
        )
        dlg.data_saved.connect(self._on_features_saved)
        dlg.exec()

    def _on_features_saved(self, data: dict):
        self._char_data["features"] = data
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Features & traits saved.")

    def _open_proficiencies_editor(self):
        dlg = ProficienciesEditor(
            char_data=self._char_data,
            existing=self._char_data.get("proficiencies"),
            parent=self,
        )
        dlg.data_saved.connect(self._on_proficiencies_saved)
        dlg.exec()

    def _on_proficiencies_saved(self, data: dict):
        self._char_data["proficiencies"] = data
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Proficiencies & languages saved.")

    def _open_equipment_editor(self):
        dlg = EquipmentEditor(
            char_data=self._char_data,
            existing=self._char_data.get("equipment"),
            parent=self,
        )
        dlg.data_saved.connect(self._on_equipment_saved)
        dlg.exec()

    def _on_equipment_saved(self, data: dict):
        self._char_data["equipment"] = data
        self._dirty = True
        self._sync_equip_to_stats(data)
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Equipment saved.")

    # ── Equipment → combat stats & attacks auto-sync ──────────────────────────

    def _sync_equip_to_stats(self, equip: dict):
        self._sync_ac_from_equipped(equip)
        self._sync_attacks_from_equipped(equip)

    def _sync_ac_from_equipped(self, equip: dict):
        from ui.editors.item_picker import ARMOR_DATA
        scores = self._char_data.get("ability_scores", {})
        dex_mod = (scores.get("DEX", 10) - 10) // 2

        equipped = [i for i in equip.get("items", []) if i.get("equipped")]
        armor_equipped = [i for i in equipped if i["name"] in ARMOR_DATA]
        if not armor_equipped:
            return

        body = [i for i in armor_equipped if ARMOR_DATA[i["name"]][1] != "shield"]
        has_shield = any(ARMOR_DATA[i["name"]][1] == "shield" for i in armor_equipped)

        ac = 10 + dex_mod
        if body:
            base, kind = ARMOR_DATA[body[0]["name"]]
            if kind == "light":
                ac = base + dex_mod
            elif kind == "medium":
                ac = base + min(dex_mod, 2)
            else:
                ac = base
        if has_shield:
            ac += 2

        combat = self._char_data.setdefault("combat_stats", {})
        if combat.get("ac") == ac:
            return
        combat["ac"] = ac
        self._rebuild_combat_preview(combat)
        self.statusBar().showMessage(f"  ⚔  Armor equipped — AC set to {ac}.")

    def _rebuild_combat_preview(self, stats: dict):
        self._sheet_view.refresh(self._char_data)

    def _sync_attacks_from_equipped(self, equip: dict):
        from ui.editors.item_picker import WEAPON_DATA
        from ui.editors.saving_throws import _prof_bonus
        scores = self._char_data.get("ability_scores", {})
        info = self._char_data.get("character_info", {})
        str_mod = (scores.get("STR", 10) - 10) // 2
        dex_mod = (scores.get("DEX", 10) - 10) // 2
        pb = _prof_bonus(info.get("level", 1))

        weapons = [i for i in equip.get("items", [])
                   if i.get("equipped") and i["name"] in WEAPON_DATA]
        equipped_names = {w["name"] for w in weapons}
        if not equipped_names:
            return

        as_data = self._char_data.setdefault("attacks_spells", {})
        # Remove any existing auto-entries for these weapons, then re-add fresh
        kept = [a for a in as_data.get("attacks", [])
                if a.get("name") not in equipped_names]

        auto = []
        for item in weapons:
            wd = WEAPON_DATA[item["name"]]
            use_dex = wd["ranged"] or (wd["finesse"] and dex_mod > str_mod)
            mod = dex_mod if use_dex else str_mod
            bonus = pb + mod
            sign = "+" if bonus >= 0 else ""
            dmg_mod = f"+{mod}" if mod > 0 else (str(mod) if mod < 0 else "")
            auto.append({
                "name":         item["name"],
                "attack_bonus": f"{sign}{bonus}",
                "damage":       f"{wd['damage']}{dmg_mod}",
                "damage_type":  wd["dmg_type"],
                "from_equipment": True,
            })

        as_data["attacks"] = kept + auto
        self._char_data["attacks_spells"] = as_data
        self._sheet_view.refresh(self._char_data)

    def _rebuild_attacks_preview(self, data: dict):
        self._sheet_view.refresh(self._char_data)

    def _open_attacks_spells_editor(self):
        dlg = AttacksSpellsEditor(
            char_data=self._char_data,
            existing=self._char_data.get("attacks_spells"),
            parent=self,
        )
        dlg.data_saved.connect(self._on_attacks_spells_saved)
        dlg.exec()

    def _on_attacks_spells_saved(self, data: dict):
        self._char_data["attacks_spells"] = data
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Attacks & spellcasting saved.")

    def _open_combat_stats_editor(self):
        dlg = CombatStatsEditor(
            char_data=self._char_data,
            existing=self._char_data.get("combat_stats"),
            parent=self,
        )
        dlg.stats_saved.connect(self._on_combat_stats_saved)
        dlg.exec()

    def _on_combat_stats_saved(self, stats: dict):
        self._char_data["combat_stats"] = stats
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Combat stats saved.")

    def _open_skills_editor(self):
        dlg = SkillsEditor(
            char_data=self._char_data,
            existing=self._char_data.get("skills"),
            parent=self,
        )
        dlg.skills_saved.connect(self._on_skills_saved)
        dlg.exec()

    def _on_skills_saved(self, skills: dict):
        self._char_data["skills"] = skills
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Skills saved.")

    def _open_ability_editor(self):
        dlg = AbilityScoreEditor(
            existing=self._char_data.get("ability_scores"),
            parent=self,
        )
        dlg.scores_saved.connect(self._on_scores_saved)
        dlg.exec()

    def _on_scores_saved(self, scores: dict):
        self._char_data["ability_scores"] = scores
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Ability scores saved.")
