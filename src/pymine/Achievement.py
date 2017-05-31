from src.pymine.event.TranslationContainer import *
from src.pymine.utils.TextFormat import *
from src.pymine.Server import *
from src.pymine.isset import *


class Achievement:
    list = {
        "mineWood": (["name", "Getting Wood"], ["requires", []]),
        "buildWorkBench": (["name", "Benchmarking"], ["requires", ["mineWood", ]]),
        "buildPickaxe": (["name", "Time to Mine!"], ["requires", ["buildWorkBench", ]]),
        "buildFurnace": (["name", "Hot Topic"], ["requires", ["buildPickaxe", ]]),
        "acquireIron": (["name", "Acquire hardware"], ["requires", ["buildFurnace", ]]),
        "buildHoe": (["name", "Time to Farm!"], ["requires", ["buildWorkBench", ]]),
        "makeBread": (["name", "Bake Bread"], ["requires", ["buildHoe", ]]),
        "bakeCake": (["name", "The Lie"], ["requires", ["buildHoe", ]]),
        "buildBetterPickaxe": (["name", "Getting an Upgrade"], ["requires", ["buildPickaxe", ]]),
        "buildSword": (["name", "Time to Strike!"], ["requires", ["buildWorkBench", ]]),
        "diamonds": (["name", "DIAMONDS!"], ["requires", ["acquireIron", ]])
    }

    def broadcast(self, player, achievementId):
        if (isset(Achievement.list[achievementId])):
            translation = TranslationContainer("chat.type.achievement", [player.getDisplayName(),
                                                                         TextFormat.GREEN +
                                                                         Achievement.list[achievementId]["name"]])
            if (Server.getInstance().getConfigString("announce-player-achievements", True) == True):
                Server.getInstance().broadcastMessage(translation)
            else:
                player.sendMessage(translation)

            return True

        return False

    def add(self, achievementId, achievementName, requires=[]):
        if (not isset(Achievement.list[achievementId])):
            Achievement.list[achievementId] = [["name", achievementName], ["requires", requires, ]]
            return True
        return False
