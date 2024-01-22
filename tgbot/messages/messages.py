from models.models import Campaign

START_MESSAGE = "Welcome to *0xScoreParser*\! 🤖\n\n" \
                "*0xScoreParser* is your bot that provides detailed information and descriptions of all the latest ongoing quests of [0xScore quests](https://app.0xscore.io/quests)\n\n" \
                "This bot will be constantly updated\. We are working to enhance new features for you\. Stay updated on all upcoming changes by using the command /updates or press *Upcoming updates* button\n\n" \
                "Don't hesitate to reach out if you have any questions or suggestions\. Enjoy your experience\!"

UPDATES_MESSAGE = "*Upcoming Updates:*\n\n" \
                  "🔔 Alerts regarding the availability of new quests\n" \
                  "📊 Personal quest completion statistics\n" \
                  "📜 Display of your currently uncompleted quests\n" \
                  "🎯 Filtering option of uncompleted quests by wallet's minimum score, prize type, number of tasks, and guaranteed score count\n\n" \
                  "We're working to help you with enchancing 0xScoreParser experience\. keep up to date with new updates\!"


def create_quest_message(quest: Campaign) -> str:
    end_date = quest.end_date.strftime('%Y %m %d') if quest.end_date else "Unlimited"
    winners_count = quest.winners_count if quest.winners_count != 0 else "Everyone"
    return \
        f"[*Link*](https://app.0xscore.io/campaign/{quest.inner_id})\n" \
        f"*Project name:* _{quest.project_name}_\n" \
        f"*Min wallet score:* _{quest.min_score}_\n" \
        f"*Rewards:*\n" \
        f"  • Reward: _{quest.reward_text}_\n" \
        f"  • Winners: _{winners_count}_\n" \
        f"  • Points: _{quest.reward_points}_\n" \
        f"*Active until*: {end_date}"

# f"[*Project twitter*]({quest.twitter_url})\n" if quest.twitter_url else ''\
# f"[*Project discord*]({quest.discord_url})\n" if quest.discord_url else ''\
# f"[*Project website*]({quest.site_url})\n" if quest.site_url else ''\

