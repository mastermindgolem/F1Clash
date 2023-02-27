import discord
from discord.commands import Option
from discord.ui import Button, View
import os
import pymongo
import time
import json
import math
import discord
from discord import Component, ActionRow, ButtonStyle, InteractionType
from discord.components import SelectOption, Button, ButtonStyle, SelectMenu
client = pymongo.MongoClient(
    "mongodb+srv://golem:OHPwJCrwdufNxsWE@f1clash.cuqr1gk.mongodb.net/?retryWrites=true&w=majority")
d = client.F1Clash
drivers = d.drivers
components = d.components
strategies = d.strategies
tyre_emoji = d.tyre_emojis
boost_emoji = d.boost_emojis



tracks = list(strategies.distinct("Track Name"))

e = tyre_emoji.find({})
tyre_replacements = {}
for i in e:
    tyre_replacements[i['Replace']] = i['Replacement']
e = boost_emoji.find({})
boost_replacements = {}
for i in e:
    boost_replacements[i['Boost'].replace(" ","").replace("-","").lower()] = i['Emoji']


bot = discord.Bot()
invite_link = "https://discord.com/api/oauth2/authorize?client_id=1011606897729732708&permissions=517543840832&scope=bot"
bot_token = open("token.txt").read()
boostedDrivers = []
boostedComps = []


async def show_drivers(ctx: discord.AutocompleteContext):
    driver_list = (["Zhou", "Magnussen", "Latifi", "Schumacher", "Albon", "Tsunoda", "Stroll", "Bottas", "Ocon", "Vettel",
                   "Ricciardo", "Perez", "Alonso", "Gasly", "Sainz", "Leclerc", "Russell", "Norris", "Verstappen", "Hamilton"])
    return ([driver for driver in driver_list if ctx.value.lower() in driver.lower()])


@bot.slash_command(guild_ids=[963621040607600680], description="Show Driver Stats")
async def driverstats(
    ctx: discord.ApplicationContext,
    driver: Option(str, "Enter Driver Name", autocomplete=show_drivers, required=True),
    rarity: Option(str, "Enter Driver Rarity", choices=["Common", "Rare", "Epic"], required=True),
    level: Option(int, "Enter Driver Level", choices=[
                  i for i in range(1, 12)], required=True)
):
    try:
        print(driver, rarity, level)
        driver_data = drivers.find_one(
            {"Name": driver, "Rarity": rarity, "Level": level})
        msg = discord.Embed(
            title=f"Level {level} {rarity} {driver}", color=discord.Color.blurple())
        msg.add_field(name="Overtaking", value=int(
            driver_data["Overtaking"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name="Defending", value=int(
            driver_data["Defending"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name="Consistency", value=int(
            driver_data["Consistency"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name="Fuel Use", value=int(
            driver_data["Fuel Use"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name="Tyre Mgmt", value=int(
            driver_data["Tyre Mgmt"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name="Wet Ability", value=int(
            driver_data["Wet Ability"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name="Max Quali", value=int(driver_data["Overtaking"]*driver_data["Multiplier"])+int(driver_data["Defending"]*driver_data["Multiplier"])+int(
            driver_data["Fuel Use"]*driver_data["Multiplier"])+int(driver_data["Tyre Mgmt"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name="Cards For Upgrade",
                      value=driver_data["Cards For Upgrade"], inline=True)
        msg.add_field(name="Total Cards Needed",
                      value=driver_data["Total Cards Needed"], inline=True)
        msg.add_field(name="Coins For Upgrade", value="{:,}".format(
            driver_data["Coins For Upgrade"]), inline=True)
        msg.add_field(name="Total Coins Needed", value="{:,}".format(
            driver_data["Total Coins Needed"]), inline=True)
        msg.add_field(name="Series", value=driver_data["Series"], inline=True)
        await ctx.respond(embed=msg, ephemeral=True)
        print("Successfully replied to command")
    except Exception as e:
        print(e)
        print(driver_data)
        await ctx.respond("An error has occured.", ephemeral=True)


async def show_comps(ctx: discord.AutocompleteContext):
    comp_list = (['Starter Brake', 'Starter Gearbox', 'Starter RearWing', 'Starter FrontWing', 'Starter Suspension', 'Starter Engine', 'The Clog', 'The Steamroller', 'Q.T.3', 'The Striker', 'Harmony', 'The Blast', 'The Crunch', 'Orbit', 'The Crest', 'The Shadow', 'Titan', 'Temper', 'Tracer', 'Symbol', 'Blitz', 'The Method', 'The Phoenix',
                 'Quicksilver', 'ApeX', 'Spectre', 'The Strongbox', 'The Whirpool', 'Prestige', 'The Momentum', 'Mirage', 'The Renegade', 'The Prodigy', 'The Catalyst', 'Scorpion', 'Wild Boar', 'The Guerilla', 'The Jazz', 'Inferno 2.0', 'C.L.A.W.', 'Spirit', 'The Menace', 'The Vindicator', 'Hydra', 'Flow', 'True Grit', 'The Flux', 'Leviathan'])
    return ([comp for comp in comp_list if ctx.value.lower().replace('.', '') in comp.lower().replace('.', '')])


@bot.slash_command(guild_ids=[963621040607600680], description="Show Component Stats")
async def compstats(
    ctx: discord.ApplicationContext,
    component: Option(str, "Enter Component Name", autocomplete=show_comps, required=True),
    level: Option(int, "Enter Component Level", choices=[
                  i for i in range(1, 12)], required=True)
):
    try:
        print(component, level)
        component_data = components.find_one(
            {"Name": component, "Level": level})
        msg = discord.Embed(
            title=f"Level {level} {component}", color=discord.Color.blurple())
        msg.add_field(
            name="Rarity", value=component_data["Rarity"], inline=True)
        msg.add_field(name="Power", value=int(
            component_data["Power"]*component_data["Multiplier"]), inline=True)
        msg.add_field(name="Aero", value=int(
            component_data["Aero"]*component_data["Multiplier"]), inline=True)
        msg.add_field(name="Grip", value=int(
            component_data["Grip"]*component_data["Multiplier"]), inline=True)
        msg.add_field(name="Reliability", value=int(
            component_data["Reliability"]*component_data["Multiplier"]), inline=True)
        msg.add_field(name="Pit Time", value=round(
            1-((1-component_data["Pit Time"])*component_data["Multiplier"]), ndigits=2), inline=True)
        msg.add_field(name="TS", value=component_data["Power"]+component_data["Aero"]+component_data["Grip"] +
                      component_data["Reliability"]+int(46-46*component_data["Pit Time"]), inline=True)
        msg.add_field(name="PAG", value=int(component_data["Power"]*component_data["Multiplier"])+int(
            component_data["Aero"]*component_data["Multiplier"])+int(component_data["Grip"]*component_data["Multiplier"]), inline=True)
        msg.add_field(name="PAGR", value=int(component_data["Power"]*component_data["Multiplier"])+int(component_data["Aero"]*component_data["Multiplier"])+int(
            component_data["Grip"]*component_data["Multiplier"])+int(component_data["Reliability"]*component_data["Multiplier"]), inline=True)
        msg.add_field(name="Cards For Upgrade",
                      value=component_data["Cards For Upgrade"], inline=False)
        msg.add_field(name="Total Cards Needed",
                      value=component_data["Total Cards Needed"], inline=False)
        msg.add_field(name="Coins For Upgrade", value="{:,}".format(
            component_data["Coins For Upgrade"]), inline=False)
        msg.add_field(name="Total Coins Needed", value="{:,}".format(
            component_data["Total Coins Needed"]), inline=False)
        msg.add_field(
            name="Series", value=component_data["Series"], inline=False)
        await ctx.respond(embed=msg, ephemeral=True)
        print("Successfully replied to command")
    except Exception as e:
        print(e)
        print(component_data)
        await ctx.respond("An error has occured.", ephemeral=True)


@bot.slash_command(guild_ids=[963621040607600680], description="Show Driver Stats")
async def comparedrivers(
    ctx: discord.ApplicationContext,
    driver1: Option(str, "Enter Driver Name", autocomplete=show_drivers, required=True),
    rarity1: Option(str, "Enter Driver Rarity", choices=["Common", "Rare", "Epic"], required=True),
    level1: Option(int, "Enter Driver Level", choices=[i for i in range(1, 12)], required=True),
    driver2: Option(str, "Enter Driver Name", autocomplete=show_drivers, required=True),
    rarity2: Option(str, "Enter Driver Rarity", choices=["Common", "Rare", "Epic"], required=True),
    level2: Option(int, "Enter Driver Level", choices=[
                   i for i in range(1, 12)], required=True)
):
    try:
        print(driver1, rarity1, level1, driver2, rarity2, level2)
        driver_data_fields = ["Overtaking", "Defending", "Consistency",
                              "Fuel Use", "Tyre Mgmt", "Wet Ability", "Max Quali", "Min Quali"]
        driver1_data = drivers.find_one(
            {"Name": driver1, "Rarity": rarity1, "Level": level1})
        driver2_data = drivers.find_one(
            {"Name": driver2, "Rarity": rarity2, "Level": level2})
        driver1_data["Max Quali"] = int(driver1_data["Overtaking"]*driver1_data["Multiplier"])+int(driver1_data["Defending"]*driver1_data["Multiplier"])+int(
            driver1_data["Fuel Use"]*driver1_data["Multiplier"])+int(driver1_data["Tyre Mgmt"]*driver1_data["Multiplier"])
        driver2_data["Max Quali"] = int(driver2_data["Overtaking"]*driver2_data["Multiplier"])+int(driver2_data["Defending"]*driver2_data["Multiplier"])+int(
            driver2_data["Fuel Use"]*driver2_data["Multiplier"])+int(driver2_data["Tyre Mgmt"]*driver2_data["Multiplier"])
        msg = discord.Embed(
            title=f"{level1} {rarity1} {driver1} | {level2} {rarity2} {driver2}", color=discord.Color.blurple())
        for field in driver_data_fields:
            if field != "Max Quali":
                driver1_data[field] = int(
                    driver1_data[field]*driver1_data["Multiplier"])
                driver2_data[field] = int(
                    driver2_data[field]*driver2_data["Multiplier"])
            msg.add_field(name=field, value=driver1_data[field], inline=True)
            msg.add_field(name=field, value=driver2_data[field], inline=True)
            if driver1_data[field] > driver2_data[field]:
                msg.add_field(
                    name="Difference", value=f"{driver1} ({round(driver1_data[field]-driver2_data[field], ndigits=2)})", inline=True)
            elif driver1_data[field] < driver2_data[field]:
                msg.add_field(
                    name="Difference", value=f"{driver2} ({round(driver2_data[field]-driver1_data[field],ndigits=2)})", inline=True)
            if driver1_data[field] == driver2_data[field]:
                msg.add_field(name="Difference", value=f"EQUAL", inline=True)

        await ctx.respond(embed=msg, ephemeral=True)
        print("Successfully replied to command")
    except Exception as e:
        print(e)
        print(driver1_data, driver2_data)
        await ctx.respond("An error has occured.", ephemeral=True)


async def show_comps(ctx: discord.AutocompleteContext):
    comp_list = (['Starter Brake', 'Starter Gearbox', 'Starter RearWing', 'Starter FrontWing', 'Starter Suspension', 'Starter Engine', 'The Clog', 'The Steamroller', 'Q.T.3', 'The Striker', 'Harmony', 'The Blast', 'The Crunch', 'Orbit', 'The Crest', 'The Shadow', 'Titan', 'Temper', 'Tracer', 'Symbol', 'Blitz', 'The Method', 'The Phoenix',
                 'Quicksilver', 'ApeX', 'Spectre', 'The Strongbox', 'The Whirpool', 'Prestige', 'The Momentum', 'Mirage', 'The Renegade', 'The Prodigy', 'The Catalyst', 'Scorpion', 'Wild Boar', 'The Guerilla', 'The Jazz', 'Inferno 2.0', 'C.L.A.W.', 'Spirit', 'The Menace', 'The Vindicator', 'Hydra', 'Flow', 'True Grit', 'The Flux', 'Leviathan'])
    return ([comp for comp in comp_list if ctx.value.lower().replace('.', '') in comp.lower().replace('.', '')])


@bot.slash_command(guild_ids=[963621040607600680], description="Show Driver Stats")
async def compareparts(
    ctx: discord.ApplicationContext,
    comp1: Option(str, "Enter Component Name", autocomplete=show_comps, required=True),
    level1: Option(int, "Enter Component Level", choices=[i for i in range(1, 12)], required=True),
    comp2: Option(str, "Enter Component Name", autocomplete=show_comps, required=True),
    level2: Option(int, "Enter Component Level", choices=[
                   i for i in range(1, 12)], required=True)
):
    try:
        print(comp1, level1, comp2, level2)
        comp_data_fields = ["Power", "Aero", "Grip",
                            "Reliability", "Pit Time", "TS", "PAG", "PAGR"]
        comp1_data = components.find_one({"Name": comp1, "Level": level1})
        comp2_data = components.find_one({"Name": comp2, "Level": level2})

        comp1_data["TS"] = comp1_data["Power"]+comp1_data["Aero"]+comp1_data["Grip"] + \
            comp1_data["Reliability"]+int(46-46*comp1_data["Pit Time"])
        comp2_data["TS"] = comp2_data["Power"]+comp2_data["Aero"]+comp2_data["Grip"] + \
            comp2_data["Reliability"]+int(46-46*comp2_data["Pit Time"])
        comp1_data["PAG"] = int(comp1_data["Power"]*comp1_data["Multiplier"])+int(
            comp1_data["Aero"]*comp1_data["Multiplier"])+int(comp1_data["Grip"]*comp1_data["Multiplier"])
        comp2_data["PAG"] = int(comp2_data["Power"]*comp2_data["Multiplier"])+int(
            comp2_data["Aero"]*comp2_data["Multiplier"])+int(comp2_data["Grip"]*comp2_data["Multiplier"])
        comp1_data["PAGR"] = int(comp1_data["Power"]*comp1_data["Multiplier"])+int(comp1_data["Aero"]*comp1_data["Multiplier"]) + \
            int(comp1_data["Grip"]*comp1_data["Multiplier"]) + \
            int(comp1_data["Aero"]*comp1_data["Multiplier"])
        comp2_data["PAGR"] = int(comp2_data["Power"]*comp2_data["Multiplier"])+int(comp2_data["Aero"]*comp2_data["Multiplier"]) + \
            int(comp2_data["Grip"]*comp2_data["Multiplier"]) + \
            int(comp2_data["Aero"]*comp1_data["Multiplier"])
        msg = discord.Embed(
            title=f"Level {level1} {comp1} | Level {level2} {comp2}", color=discord.Color.blurple())
        for field in comp_data_fields:
            msg.add_field(name=field, value=comp1_data[field], inline=True)
            msg.add_field(name=field, value=comp2_data[field], inline=True)
            comp1_data[field] = round(float(comp1_data[field]), ndigits=0)
            comp2_data[field] = round(float(comp2_data[field]), ndigits=0)
            if comp1_data[field] > comp2_data[field]:
                msg.add_field(
                    name="Difference", value=f"{comp1} ({round(comp1_data[field]-comp2_data[field],ndigits=2)})", inline=True)
            elif comp1_data[field] < comp2_data[field]:
                msg.add_field(
                    name="Difference", value=f"{comp2} ({round(comp2_data[field]-comp1_data[field],ndigits=2)})", inline=True)
            if comp1_data[field] == comp2_data[field]:
                msg.add_field(name="Difference", value=f"EQUAL", inline=True)

        await ctx.respond(embed=msg, ephemeral=True)
        print("Successfully replied to command")
    except Exception as e:
        print(e)
        print(comp1_data, comp2_data)
        await ctx.respond("An error has occured.", ephemeral=True)


async def show_all(ctx: discord.AutocompleteContext):
    comp_list = (["Zhou", "Magnussen", "Latifi", "Schumacher", "Albon", "Tsunoda", "Stroll", "Bottas", "Ocon", "Vettel", "Ricciardo", "Perez", "Alonso", "Gasly", "Sainz", "Leclerc", "Russell", "Norris", "Verstappen", "Hamilton", 'Starter Brake', 'Starter Gearbox', 'Starter RearWing', 'Starter FrontWing', 'Starter Suspension', 'Starter Engine', 'The Clog', 'The Steamroller', 'Q.T.3', 'The Striker', 'Harmony', 'The Blast', 'The Crunch', 'Orbit',
                 'The Crest', 'The Shadow', 'Titan', 'Temper', 'Tracer', 'Symbol', 'Blitz', 'The Method', 'The Phoenix', 'Quicksilver', 'ApeX', 'Spectre', 'The Strongbox', 'The Whirpool', 'Prestige', 'The Momentum', 'Mirage', 'The Renegade', 'The Prodigy', 'The Catalyst', 'Scorpion', 'Wild Boar', 'The Guerilla', 'The Jazz', 'Inferno 2.0', 'C.L.A.W.', 'Spirit', 'The Menace', 'The Vindicator', 'Hydra', 'Flow', 'True Grit', 'The Flux', 'Leviathan'])
    return ([comp for comp in comp_list if ctx.value.lower().replace('.', '') in comp.lower().replace('.', '')])


@bot.slash_command(guild_ids=[963621040607600680], description="Boost a driver/comp")
async def boost(
    ctx: discord.AutocompleteContext,
    asset: Option(str, "Enter Asset to Boost", autocomplete=show_all, required=True),
    multiplier: Option(float, "Enter Multiplier", required=True)
):
    await ctx.defer()
    response = await ctx.respond("Updating multipliers...", ephemeral=True)
    if asset in drivers.distinct("Name"):
        for rarity in drivers.find({"Name": asset}).distinct("Rarity"):
            for level in drivers.find({"Name": asset, "Rarity": rarity}).distinct("Level"):
                drivers.find_one_and_update({"Name": asset, "Level": level, "Rarity": rarity}, {
                                            "$set": {"Multiplier": float(multiplier)}})
                await response.edit(content=f"Level {level} {rarity} updated.", ephemeral=True)
        await ctx.respond(f"Updated {asset}'s multiplier to {multiplier}.", ephemeral=True)
    elif asset in components.distinct("Name"):
        for level in components.find({"Name": asset}).distinct("Level"):
            components.find_one_and_update({"Name": asset, "Level": level}, {
                                           "$set": {"Multiplier": float(multiplier)}})
            await response.edit(content=f"Level {level} updated.", ephemeral=True)
        await ctx.respond(f"Updated {asset}'s multiplier to {multiplier}.", ephemeral=True)
    else:
        await ctx.respond("An error has occured.", ephemeral=True)





class PageButton(discord.ui.Button):
    def __init__(self, page_name: str, page_color: ButtonStyle, page: discord.Embed, custom_id: str, row: int):
        super().__init__(
            label=page_name,
            style=page_color,
            custom_id=custom_id,
            row=row
        )
        self.callback_page = page

    async def callback(self, interaction: discord.Interaction):
        await interaction.message.edit(embed=self.callback_page)
        await interaction.response.defer()

def add_tyre_emoji(content: str):
    for r in tyre_replacements:
        content = content.replace(r, tyre_replacements[r])
    return content


def add_boost_emoji(content: str):
    if content.replace(" ","").replace("-","").lower() in boost_replacements:
        return content + boost_replacements[content.replace(" ","").replace("-","").lower()]
    else:
        return content


async def show_tracks(ctx: discord.AutocompleteContext):
    return ([track for track in tracks if ctx.value.lower().replace('.', '') in track.lower()])


@bot.slash_command(guild_ids=[963621040607600680], description="Show track strategy")
async def strategy(
    ctx: discord.AutocompleteContext,
    track: Option(str, "Enter Track", autocomplete=show_tracks, required=True)
):
    global tracks
    if ctx.channel.id != 1079430826904784996:
        await ctx.respond("Please use this command in <#1079430826904784996> instead.", ephemeral=True)
        return
    await ctx.defer()
    response = await ctx.respond("Fetching strategies...", ephemeral=True)
    strategy = strategies.find_one({"Track Name": track})
    page1 = discord.Embed(title=f"Front Strategy for {track}", color=discord.Color.brand_red())
    page2 = discord.Embed(title=f"Mid Strategy for {track}", color=discord.Color.brand_green())
    page3 = discord.Embed(title=f"Back Strategy for {track}", color=discord.Color.blurple())
    page4 = discord.Embed(title=f"Characteristics of {track}", color=discord.Color.lighter_grey())
    
    pages = [page1, page2, page3, page4]
    
    for strat_type in ["Dry", "Wet"]:
        if strat_type in strategy:
            for start_pos in ["Front", "Mid", "Back"]:
                page_index = ["Front", "Mid", "Back"].index(start_pos)
                if start_pos in strategy[strat_type]:
                    n = len(strategy[strat_type][start_pos])
                    if n == 1:
                        value = f"D1 : {add_tyre_emoji(strategy[strat_type][start_pos][0]['strategy1'])} : {add_boost_emoji(strategy[strat_type][start_pos][0]['boost1'])}"
                        value = value + f"\nD2 : {add_tyre_emoji(strategy[strat_type][start_pos][0]['strategy2'])} : {add_boost_emoji(strategy[strat_type][start_pos][0]['boost2'])}"
                        pages[page_index].add_field(name=f"{strat_type} Strategy", value = value, inline = False)
                    else:
                        for i in range(n):
                            value = f"D1 : {add_tyre_emoji(strategy[strat_type][start_pos][i]['strategy1'])} : {add_boost_emoji(strategy[strat_type][start_pos][i]['boost1'])}"
                            value = value + f"\nD2 : {add_tyre_emoji(strategy[strat_type][start_pos][i]['strategy2'])} : {add_boost_emoji(strategy[strat_type][start_pos][i]['boost2'])}"
                            pages[page_index].add_field(name=f"{strat_type} Strategy {i+1}", value = value, inline = False)
        
    pages[3].add_field(name="Characteristics", value="\n".join(
        strategy['Characteristics']), inline=False)
    pages[3].add_field(name="Overtaking Zones", value="Turn " + "\n Turn ".join(
        [str(i) for i in strategy['Overtaking Zones']]), inline=False)
    pages[3].set_image(url=strategy['Track Image'])

    view = discord.ui.View(timeout=None)
    
    view.add_item(PageButton(page_name="Front Strat", page_color=ButtonStyle.red, page=pages[0], custom_id="page1", row=0))
    view.add_item(PageButton(page_name="Mid Strat", page_color=ButtonStyle.green, page=pages[1], custom_id="page2", row=0))
    view.add_item(PageButton(page_name="Back Strat", page_color=ButtonStyle.blurple, page=pages[2], custom_id="page3", row=0))
    view.add_item(EditStratButton(track=track))
    view.add_item(PageButton(page_name="Track Info", page_color=ButtonStyle.grey, page=pages[3], custom_id="page4", row=1))
    view.add_item(EditInfoButton(track=track))

    await response.edit(content="", embed=page1, view=view)
    tracks = strategies.distinct("Track Name")



class EditStratButton(discord.ui.Button):
    def __init__(self, track):
        super().__init__(
            label="Edit Strat",
            style=ButtonStyle.danger,
            custom_id="edit_strat",
            row=0
        )
        self.track = track

    async def callback(self, interaction: discord.Interaction):
        self.start_pos = interaction.message.embeds[0].title.split(" ")[0]
        self.title = f"Editing {self.start_pos} Strategy for {self.track.split(',')[0]}"
        modal = EditStrategy(track=self.track, start_pos=self.start_pos, title=self.title)
        await interaction.response.send_modal(modal)

class EditStrategy(discord.ui.Modal):
    def __init__(self, track, start_pos, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.add_item(discord.ui.InputText(label="Condition (Dry/Wet)", style=discord.InputTextStyle.singleline, min_length=3, max_length=3, placeholder='Input the race condition (Must be "Dry" or "Wet")', required=True))
        self.add_item(discord.ui.InputText(label="D1 Strategy", style=discord.InputTextStyle.singleline, placeholder="Driver 1's tyre strategy", required=False))
        self.add_item(discord.ui.InputText(label="D1 Boost", style=discord.InputTextStyle.singleline, placeholder="Driver 1's boost", required=False))
        self.add_item(discord.ui.InputText(label="D2 Strategy", style=discord.InputTextStyle.singleline, placeholder="Driver 2's tyre strategy", required=False))
        self.add_item(discord.ui.InputText(label="D2 Boost", style=discord.InputTextStyle.singleline, placeholder="Driver 2's boost", required=False))
        self.track = track
        self.start_pos = start_pos
        
    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Editing {self.start_pos} Strategy for {self.track}")
        condition = self.children[0].value
        if self.children[1].value != None:
            d1_s = str(self.children[1].value).replace(" / "," | ").replace(" - "," | ").replace("/"," | ").replace("-"," | ").upper()
            embed.add_field(name="Driver 1 Strategy", value=d1_s)
        if self.children[2].value != None:
            d1_b = str(self.children[2].value)
            embed.add_field(name="Driver 1 Boost", value=d1_b)
        if self.children[3].value != None:
            d2_s = str(self.children[3].value).replace(" / "," | ").replace(" - "," | ").replace("/"," | ").replace("-"," | ").upper()
            embed.add_field(name="Driver 2 Strategy", value=d2_s)
        if self.children[4].value != None:
            d2_b = str(self.children[4].value)
            embed.add_field(name="Driver 2 Boost", value=d2_b)
            
        current_strategy = strategies.find_one({"Track Name": self.track})
        
        if condition not in current_strategy:
            current_strategy[condition] = {"Front": [], "Mid": [], "Back": []}
        current_strategy[condition][self.start_pos].append({"strategy1": d1_s, "boost1": d1_b, "strategy2": d2_s, "boost2": d2_b})
        strategies.find_one_and_replace({"Track Name": self.track},current_strategy)
        
        
        await interaction.response.send_message(embeds=[embed], ephemeral=True)

class EditInfoButton(discord.ui.Button):
    def __init__(self, track):
        super().__init__(
            label="Edit Info",
            style=ButtonStyle.danger,
            custom_id="edit_info",
            row=1
        )
        self.track = track

    async def callback(self, interaction: discord.Interaction):
        self.title = f"Editing Track Info for {self.track.split(',')[0]}"
        modal = EditInfo(track=self.track, title=self.title)
        await interaction.response.send_modal(modal)

class EditInfo(discord.ui.Modal):
    def __init__(self, track, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.track = track
        self.current_strategy = strategies.find_one({"Track Name": self.track})
        if "Characteristics" not in self.current_strategy:
            self.current_strategy["Characteristics"] = ""
        self.add_item(discord.ui.InputText(label='Characteristics (Separate with ", ")', style=discord.InputTextStyle.singleline, placeholder = ", ".join(self.current_strategy["Characteristics"]), required=False))
        if "Overtaking Zones" not in self.current_strategy:
            self.current_strategy["Overtaking Zones"] = []
        self.add_item(discord.ui.InputText(label="Overtaking Zones (Integers only)", style=discord.InputTextStyle.singleline, placeholder=" ".join([str(i) for i in self.current_strategy["Overtaking Zones"]]), required=False))
        
    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title=f"Editing Track Info for {self.track}")
        if self.children[0].value != None:
            c = str(self.children[0].value).split(", ")
            if c == []:
                c = self.current_strategy["Characteristics"]
            embed.add_field(name="Characteristics ", value=c)
            self.current_strategy["Characteristics"] = c
        if self.children[1].value != None:
            otz = [int(i) for i in str(self.children[1].value).split(" ")]
            if otz == []:
                otz = self.current_strategy["Overtaking Zones"]
            embed.add_field(name="Overtaking Zones", value=otz)
            self.current_strategy["Overtaking Zones"] = otz
            
        
        
        strategies.find_one_and_replace({"Track Name": self.track},self.current_strategy)
        
        
        await interaction.response.send_message(embeds=[embed], ephemeral=True)

@bot.slash_command(guild_ids=[963621040607600680], description="Show all available commands")
async def help(
    ctx: discord.AutocompleteContext
):
    embed = discord.Embed(title = "Morgan F1 Bot Commands", color=discord.Color.blurple())
    embed.add_field(name="`/help`", value = "Displays this help message.", inline=False)
    embed.add_field(name="`/driverstats [driver] [rarity] [level]`", value = "Displays the stats for a certain driver at a given rarity and level. All fields are required.", inline=False)
    embed.add_field(name="`/compstats [component] [level]`", value = "Display the stats for a component at a given level. All fields are required.", inline=False)
    embed.add_field(name="`/comparedrivers [driver1] [rarity1] [level1] [driver2] [rarity2] [level2]`", value = "Compares the stats for 2 drivers. All fields are required.", inline=False)
    embed.add_field(name="`/compareparts [componen1] [level1] [component2] [level2]`", value = "Compares the stats for 2 components. All fields are required.", inline=False)
    embed.add_field(name="`/boost [driver/component] [multiplier]`", value = "Boosts/Unboosts an asset by the multiplier. Used for stat boosts during GP events. All fields are required.", inline=True)
    embed.add_field(name="`/strategy [track]`", value = "Displays the strategies for that track, sorted into front/mid/back of the grid based on your starting position.\nCan navigate through each set of strategies using the buttons at the bottom.\nTrack Info page gives a map of the track, along with the best stats to have on that track, along with overtaking zones.\nEdit Info button to be used to add any strategy to the current page you are on. Make sure the boost is a valid boost, and enter the correct race condition.", inline=False)
    await ctx.respond(embeds = [embed])


@bot.event
async def on_ready():
    print('Bot is online!')


bot.run(bot_token)
