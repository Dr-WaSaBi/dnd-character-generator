# ╔══════════════════════════════════════════════════════════════════════╗
# ║     ⚔  D&D 5e CHARACTER GENERATOR  ⚔                               ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  File    : ui/character_sheet.py                                     ║
# ║  Created : 2026-05-13                                                ║
# ║  Version : 1.0.1                                                     ║
# ╠══════════════════════════════════════════════════════════════════════╣
# ║  Main application window. Owns the character data dict, file I/O,   ║
# ║  menu bar, and routes section-click signals to the right editor      ║
# ║  dialog, then syncs results back into the sheet view.                ║
# ╚══════════════════════════════════════════════════════════════════════╝

import json
import os
import traceback

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
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
        """Initialize the main window, apply the theme, and build the UI and menu."""
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
        """Construct the central widget: a scrollable SheetView paired with the DiceRollerPanel."""
        from ui.dice_roller import DiceRollerPanel

        outer = QWidget()
        outer.setStyleSheet(f"background-color: {COLOR_WINDOW_BG};")
        self.setCentralWidget(outer)
        outer_lo = QVBoxLayout(outer)
        outer_lo.setContentsMargins(12, 12, 12, 12)

        content = QHBoxLayout()
        content.setSpacing(8)
        content.setContentsMargins(0, 0, 0, 0)
        outer_lo.addLayout(content, 1)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self._sheet_view = SheetView()
        self._sheet_view.section_clicked.connect(self._on_section_clicked)
        scroll.setWidget(self._sheet_view)

        self._dice_panel = DiceRollerPanel()
        self._sheet_view.weapon_attacked.connect(self._dice_panel.weapon_attack)

        content.addWidget(scroll, 1)
        content.addWidget(self._dice_panel)

        self.statusBar().setFixedHeight(26)
        self.statusBar().showMessage(
            "  Click any section to edit  ·  Click a weapon row to roll attack & damage"
        )

    # ── Menu bar ─────────────────────────────────────────────────────────────

    def _build_menu(self):
        """Build the File menu with New, Open, Save, Save As, Starting Equipment, Export PDF, and Quit actions."""
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
        """Clear all character data and reset the sheet to a blank state, prompting to save if dirty."""
        if self._dirty and not self._confirm_discard():
            return
        self._char_data = {}
        self._current_file = None
        self._dirty = False
        self._reset_sheet()
        self.setWindowTitle("D&D 5e Character Generator")
        self.statusBar().showMessage("  New character — select a section to begin.")

    def _on_starting_equipment(self):
        """Open the StartingEquipmentDialog and connect its signal to apply the chosen gear."""
        dlg = StartingEquipmentDialog(char_data=self._char_data, parent=self)
        dlg.equipment_chosen.connect(self._apply_starting_equipment)
        dlg.exec()

    def _apply_starting_equipment(self, items: list, gold_gp: int):
        """Merge class starting items and gold into the equipment section and refresh the view."""
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
        """Show a file picker, load the selected .dnd5e JSON file, and refresh the sheet."""
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
        """Save to the current file path, or delegate to Save As if no path is set."""
        if self._current_file:
            self._write_file(self._current_file)
        else:
            self._on_save_as()

    def _on_save_as(self):
        """Prompt the user for a save path and write the character data there."""
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
        """Serialize _char_data to indented JSON and write it to path, clearing the dirty flag."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self._char_data, f, indent=2)
            self._dirty = False
            self.statusBar().showMessage(f"  ✔  Saved: {os.path.basename(path)}")
        except Exception as exc:
            QMessageBox.critical(self, "Save failed", str(exc))

    def _on_export_pdf(self):
        """Prompt for a PDF path and call export_pdf() to render the two-page character sheet."""
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
        """Ask the user whether to save, discard, or cancel when there are unsaved changes. Returns True if the caller may proceed."""
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
        """Intercept the window-close event and offer to save unsaved changes before quitting."""
        if self._dirty and not self._confirm_discard():
            event.ignore()
        else:
            event.accept()

    def _reset_sheet(self):
        """Clear the sheet view by refreshing it with an empty data dict."""
        self._sheet_view.refresh({})

    def _apply_loaded_data(self):
        """Push the loaded character data into the sheet view and clear the dirty flag."""
        self._sheet_view.refresh(self._char_data)
        self._dirty = False

    def _on_section_clicked(self, number: int):
        """Dispatch a numbered section click (1–10) to the appropriate editor dialog."""
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
        """Open the CharacterInfoEditor dialog pre-populated with current info data."""
        dlg = CharacterInfoEditor(
            existing=self._char_data.get("character_info"),
            parent=self,
        )
        dlg.info_saved.connect(self._on_info_saved)
        dlg.exec()

    def _on_info_saved(self, info: dict):
        """Store saved character info, mark dirty, and refresh the sheet view."""
        self._char_data["character_info"] = info
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Character info saved.")

    def _open_saving_throws_editor(self):
        """Open the SavingThrowEditor dialog, passing full char_data for proficiency calculations."""
        dlg = SavingThrowEditor(
            char_data=self._char_data,
            existing=self._char_data.get("saving_throws"),
            parent=self,
        )
        dlg.throws_saved.connect(self._on_throws_saved)
        dlg.exec()

    def _on_throws_saved(self, throws: dict):
        """Store saved saving throw data, mark dirty, and refresh the sheet view."""
        self._char_data["saving_throws"] = throws
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Saving throws saved.")

    def _open_personality_editor(self):
        """Open the PersonalityEditor dialog with current personality data."""
        dlg = PersonalityEditor(
            existing=self._char_data.get("personality"),
            parent=self,
        )
        dlg.data_saved.connect(self._on_personality_saved)
        dlg.exec()

    def _on_personality_saved(self, data: dict):
        """Store saved personality data, mark dirty, and refresh the sheet view."""
        self._char_data["personality"] = data
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Personality saved.")

    def _open_features_editor(self):
        """Open the FeaturesEditor dialog with current features data and full char_data context."""
        dlg = FeaturesEditor(
            char_data=self._char_data,
            existing=self._char_data.get("features"),
            parent=self,
        )
        dlg.data_saved.connect(self._on_features_saved)
        dlg.exec()

    def _on_features_saved(self, data: dict):
        """Store saved features data, mark dirty, and refresh the sheet view."""
        self._char_data["features"] = data
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Features & traits saved.")

    def _open_proficiencies_editor(self):
        """Open the ProficienciesEditor dialog with current proficiency and language data."""
        dlg = ProficienciesEditor(
            char_data=self._char_data,
            existing=self._char_data.get("proficiencies"),
            parent=self,
        )
        dlg.data_saved.connect(self._on_proficiencies_saved)
        dlg.exec()

    def _on_proficiencies_saved(self, data: dict):
        """Store saved proficiency data, mark dirty, and refresh the sheet view."""
        self._char_data["proficiencies"] = data
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Proficiencies & languages saved.")

    def _open_equipment_editor(self):
        """Open the EquipmentEditor dialog with current equipment and currency data."""
        dlg = EquipmentEditor(
            char_data=self._char_data,
            existing=self._char_data.get("equipment"),
            parent=self,
        )
        dlg.data_saved.connect(self._on_equipment_saved)
        dlg.exec()

    def _on_equipment_saved(self, data: dict):
        """Store saved equipment, trigger AC and weapon auto-sync, mark dirty, and refresh."""
        self._char_data["equipment"] = data
        self._dirty = True
        self._sync_equip_to_stats(data)
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Equipment saved.")

    # ── Equipment → combat stats & attacks auto-sync ──────────────────────────

    def _sync_equip_to_stats(self, equip: dict):
        """Run both AC and weapon-attack auto-sync passes whenever equipment changes."""
        self._sync_ac_from_equipped(equip)
        self._sync_attacks_from_equipped(equip)

    def _sync_ac_from_equipped(self, equip: dict):
        """Derive AC from the currently equipped armor and shield, then write it into combat_stats."""
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
        """Refresh the sheet view after combat stats are updated by auto-sync."""
        self._sheet_view.refresh(self._char_data)

    def _sync_attacks_from_equipped(self, equip: dict):
        """Auto-generate attack entries for all equipped weapons, replacing any previous auto-entries."""
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
        """Refresh the sheet view after attacks data changes."""
        self._sheet_view.refresh(self._char_data)

    def _open_attacks_spells_editor(self):
        """Open the AttacksSpellsEditor dialog with current attacks and spell slot data."""
        dlg = AttacksSpellsEditor(
            char_data=self._char_data,
            existing=self._char_data.get("attacks_spells"),
            parent=self,
        )
        dlg.data_saved.connect(self._on_attacks_spells_saved)
        dlg.exec()

    def _on_attacks_spells_saved(self, data: dict):
        """Store saved attacks/spells data, mark dirty, and refresh the sheet view."""
        self._char_data["attacks_spells"] = data
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Attacks & spellcasting saved.")

    def _open_combat_stats_editor(self):
        """Open the CombatStatsEditor dialog with current HP, AC, and condition data."""
        dlg = CombatStatsEditor(
            char_data=self._char_data,
            existing=self._char_data.get("combat_stats"),
            parent=self,
        )
        dlg.stats_saved.connect(self._on_combat_stats_saved)
        dlg.exec()

    def _on_combat_stats_saved(self, stats: dict):
        """Store saved combat stats, mark dirty, and refresh the sheet view."""
        self._char_data["combat_stats"] = stats
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Combat stats saved.")

    def _open_skills_editor(self):
        """Open the SkillsEditor dialog with current skill proficiency data."""
        dlg = SkillsEditor(
            char_data=self._char_data,
            existing=self._char_data.get("skills"),
            parent=self,
        )
        dlg.skills_saved.connect(self._on_skills_saved)
        dlg.exec()

    def _on_skills_saved(self, skills: dict):
        """Store saved skills data, mark dirty, and refresh the sheet view."""
        self._char_data["skills"] = skills
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Skills saved.")

    def _open_ability_editor(self):
        """Open the AbilityScoreEditor dialog with the current six ability scores."""
        dlg = AbilityScoreEditor(
            existing=self._char_data.get("ability_scores"),
            parent=self,
        )
        dlg.scores_saved.connect(self._on_scores_saved)
        dlg.exec()

    def _on_scores_saved(self, scores: dict):
        """Store saved ability scores, mark dirty, and refresh the sheet view."""
        self._char_data["ability_scores"] = scores
        self._dirty = True
        self._sheet_view.refresh(self._char_data)
        self.statusBar().showMessage("  ✔  Ability scores saved.")
