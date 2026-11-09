"""Regression tests for the original Siber Savaş game mechanics.

Run from the project root with:
    python -m unittest discover -s tests -v
"""
from contextlib import redirect_stdout
from io import StringIO
import unittest
from unittest.mock import patch

from siber_savas import (
    AgFedaisi,
    DijitalVarlik,
    KodAvcisi,
    Virus,
    karakter_olustur,
    menu_secimi_al,
    rastgele_dusman_uret,
    savas_dongusu,
    zorunlu_metin_al,
)


class EntityTests(unittest.TestCase):
    def test_damage_reduces_health(self):
        entity = DijitalVarlik("Test Entity", guc=10, can=50)

        with redirect_stdout(StringIO()):
            entity.hasar_al(15)

        self.assertEqual(entity.can, 35)
        self.assertTrue(entity.canli_mi())

    def test_damage_does_not_reduce_health_below_zero(self):
        entity = DijitalVarlik("Test Entity", guc=10, can=20)

        with redirect_stdout(StringIO()):
            entity.hasar_al(100)

        self.assertEqual(entity.can, 0)
        self.assertFalse(entity.canli_mi())

    def test_defending_reduces_incoming_damage_to_one_third(self):
        player = KodAvcisi("Player")
        enemy = Virus("Test Virus", guc=20, can=40)

        with redirect_stdout(StringIO()):
            enemy.saldir(player, oyuncu_savunmada_mi=True)

        self.assertEqual(player.can, 80 - (20 // 3))


class CharacterAbilityTests(unittest.TestCase):
    def test_code_hunter_special_ability_deals_double_damage(self):
        player = KodAvcisi("Player")
        enemy = Virus("Test Virus", guc=10, can=100)

        with redirect_stdout(StringIO()):
            player.ozel_guc(enemy)

        self.assertEqual(enemy.can, 20)
        self.assertEqual(player.ozel_guc_hakki, 4)

    def test_code_hunter_cannot_use_special_ability_without_charges(self):
        player = KodAvcisi("Player")
        enemy = Virus("Test Virus", guc=10, can=100)
        player.ozel_guc_hakki = 0

        with redirect_stdout(StringIO()):
            player.ozel_guc(enemy)

        self.assertEqual(enemy.can, 100)
        self.assertEqual(player.ozel_guc_hakki, 0)

    def test_network_defender_heals_without_exceeding_max_health(self):
        player = AgFedaisi("Player")
        player.can = 90
        enemy = Virus("Test Virus", guc=10, can=100)

        with redirect_stdout(StringIO()):
            player.ozel_guc(enemy)

        self.assertEqual(player.can, player.max_can)
        self.assertEqual(player.ozel_guc_hakki, 4)

    def test_network_defender_special_ability_does_not_overheal(self):
        player = AgFedaisi("Player")
        enemy = Virus("Test Virus", guc=10, can=100)

        with redirect_stdout(StringIO()):
            player.ozel_guc(enemy)

        self.assertEqual(player.can, player.max_can)


class EnemyGenerationTests(unittest.TestCase):
    @patch("siber_savas.random.choice", return_value=("Trojan Test", 15, 60))
    def test_regular_enemy_stats_scale_with_level(self, mocked_choice):
        enemy = rastgele_dusman_uret(2)

        self.assertEqual(enemy.ad, "Trojan Test")
        self.assertEqual(enemy.guc, 18)
        self.assertEqual(enemy.can, 72)
        mocked_choice.assert_called_once()

    def test_boss_is_generated_every_fifth_level(self):
        boss = rastgele_dusman_uret(5)

        self.assertIn("BOSS", boss.ad)
        self.assertEqual(boss.guc, 52)
        self.assertEqual(boss.can, 225)

    def test_boss_stats_scale_at_level_ten(self):
        boss = rastgele_dusman_uret(10)

        self.assertIn("BOSS", boss.ad)
        self.assertEqual(boss.guc, 70)
        self.assertEqual(boss.can, 300)


class InputValidationTests(unittest.TestCase):
    def test_empty_player_name_is_rejected_until_non_empty_value_is_entered(self):
        with patch("builtins.input", side_effect=["   ", "Kadir"]):
            with redirect_stdout(StringIO()):
                player_name = zorunlu_metin_al("Player name: ")

        self.assertEqual(player_name, "Kadir")

    def test_menu_choice_is_normalized_and_invalid_values_are_rejected(self):
        with patch("builtins.input", side_effect=["invalid", " E "]):
            with redirect_stdout(StringIO()):
                choice = menu_secimi_al(("e", "h"), "Continue? ")

        self.assertEqual(choice, "e")

    def test_character_creation_retries_invalid_class_selection(self):
        with patch("builtins.input", side_effect=["Kadir", "0", "2"]):
            with redirect_stdout(StringIO()):
                player = karakter_olustur()

        self.assertIsInstance(player, AgFedaisi)
        self.assertEqual(player.ad, "Kadir")

    def test_invalid_battle_command_does_not_give_enemy_a_free_turn(self):
        player = KodAvcisi("Kadir")
        enemy = Virus("Test Virus", guc=20, can=20)

        with patch("builtins.input", side_effect=["invalid", "1"]), \\
             patch("siber_savas.time.sleep"), \\
             redirect_stdout(StringIO()):
            result = savas_dongusu(player, enemy)

        self.assertTrue(result)
        self.assertEqual(player.can, player.max_can)
        self.assertFalse(enemy.canli_mi())


if __name__ == "__main__":
    unittest.main()
