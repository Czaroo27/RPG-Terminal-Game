def check_quests(player):
    if player.level >= 5 and not hasattr(player, "quest_level5_completed"):
        print("🎉 Quest Completed: Reach Level 5!")
        player.gold += 100
        print("You received 100 gold as a reward!")
        player.quest_level5_completed = True
