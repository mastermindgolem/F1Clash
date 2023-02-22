import discord
from discord.commands import Option
from discord.ui import Button, View
import os, pymongo, time, json, math, discord
client = pymongo.MongoClient("mongodb+srv://golem:OHPwJCrwdufNxsWE@f1clash.cuqr1gk.mongodb.net/?retryWrites=true&w=majority")
d = client.F1Clash
drivers = d.drivers
components = d.components



bot = discord.Bot()
invite_link = "https://discord.com/api/oauth2/authorize?client_id=1011606897729732708&permissions=517543840832&scope=bot"
bot_token = json.loads(open("config.json").read())["token"]
boostedDrivers = []
boostedComps = []


async def show_drivers(ctx: discord.AutocompleteContext):
    driver_list = (["Zhou","Magnussen","Latifi","Schumacher","Albon","Tsunoda","Stroll","Bottas","Ocon","Vettel","Ricciardo","Perez","Alonso","Gasly","Sainz","Leclerc","Russell","Norris","Verstappen","Hamilton"])
    return([driver for driver in driver_list if ctx.value.lower() in driver.lower()])
@bot.slash_command(guild_ids=[963621040607600680], description = "Show Driver Stats")
async def driverstats(
    ctx: discord.ApplicationContext,
    driver: Option(str, "Enter Driver Name", autocomplete = show_drivers, required = True),
    rarity: Option(str, "Enter Driver Rarity", choices = ["Common", "Rare", "Epic"], required = True),
    level: Option(int, "Enter Driver Level", choices = [i for i in range(1,12)], required = True)
):
    try:
        print(driver, rarity, level)
        driver_data = drivers.find_one({"Name": driver, "Rarity": rarity, "Level": level})
        msg = discord.Embed(title = f"Level {level} {rarity} {driver}", color = discord.Color.blurple())
        msg.add_field(name = "Overtaking", value = int(driver_data["Overtaking"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name = "Defending", value = int(driver_data["Defending"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name = "Consistency", value = int(driver_data["Consistency"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name = "Fuel Use", value = int(driver_data["Fuel Use"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name = "Tyre Mgmt", value = int(driver_data["Tyre Mgmt"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name = "Wet Ability", value = int(driver_data["Wet Ability"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name = "Max Quali", value = int(driver_data["Overtaking"]*driver_data["Multiplier"])+int(driver_data["Defending"]*driver_data["Multiplier"])+int(driver_data["Fuel Use"]*driver_data["Multiplier"])+int(driver_data["Tyre Mgmt"]*driver_data["Multiplier"]), inline=True)
        msg.add_field(name = "Spread", value = int(9930/(driver_data["Consistency"]*driver_data["Multiplier"])-103.74), inline=True)
        msg.add_field(name = "Min Quali", value = int(driver_data["Overtaking"]*driver_data["Multiplier"])+int(driver_data["Defending"]*driver_data["Multiplier"])+int(driver_data["Fuel Use"]*driver_data["Multiplier"])+int(driver_data["Tyre Mgmt"]*driver_data["Multiplier"]) - int(9930/(driver_data["Consistency"]*driver_data["Multiplier"])-103.74), inline=True)
        msg.add_field(name = "Cards For Upgrade", value = driver_data["Cards For Upgrade"], inline=False)
        msg.add_field(name = "Total Cards Needed", value = driver_data["Total Cards Needed"], inline=False)
        msg.add_field(name = "Coins For Upgrade", value = "{:,}".format(driver_data["Coins For Upgrade"]), inline=False)
        msg.add_field(name = "Total Coins Needed", value = "{:,}".format(driver_data["Total Coins Needed"]), inline=False)
        msg.add_field(name = "Series", value = driver_data["Series"], inline=False)
        await ctx.respond(embed = msg, ephemeral = True)
        print("Successfully replied to command")
    except Exception as e:
        print(e)
        print(driver_data)
        await ctx.respond("An error has occured.", ephemeral = True)
        
        
async def show_comps(ctx: discord.AutocompleteContext):
    comp_list = (['Starter Brake', 'Starter Gearbox', 'Starter RearWing', 'Starter FrontWing', 'Starter Suspension', 'Starter Engine', 'The Clog', 'The Steamroller', 'Q.T.3', 'The Striker', 'Harmony', 'The Blast', 'The Crunch', 'Orbit', 'The Crest', 'The Shadow', 'Titan', 'Temper', 'Tracer', 'Symbol', 'Blitz', 'The Method', 'The Phoenix', 'Quicksilver', 'ApeX', 'Spectre', 'The Strongbox', 'The Whirpool', 'Prestige', 'The Momentum', 'Mirage', 'The Renegade', 'The Prodigy', 'The Catalyst', 'Scorpion', 'Wild Boar', 'The Guerilla', 'The Jazz', 'Inferno 2.0', 'C.L.A.W.', 'Spirit', 'The Menace', 'The Vindicator', 'Hydra', 'Flow', 'True Grit', 'The Flux', 'Leviathan'])
    return([comp for comp in comp_list if ctx.value.lower().replace('.','') in comp.lower().replace('.','')])
@bot.slash_command(guild_ids=[963621040607600680], description = "Show Component Stats")
async def compstats(
    ctx: discord.ApplicationContext,
    component: Option(str, "Enter Component Name", autocomplete = show_comps, required = True),
    level: Option(int, "Enter Component Level", choices = [i for i in range(1,12)], required = True)
):
    try:
        print(component, level)
        component_data = components.find_one({"Name": component, "Level": level})
        msg = discord.Embed(title = f"Level {level} {component}", color = discord.Color.blurple())
        msg.add_field(name = "Rarity", value = component_data["Rarity"], inline=True)
        msg.add_field(name = "Power", value = int(component_data["Power"]*component_data["Multiplier"]), inline=True)
        msg.add_field(name = "Aero", value = int(component_data["Aero"]*component_data["Multiplier"]), inline=True)
        msg.add_field(name = "Grip", value = int(component_data["Grip"]*component_data["Multiplier"]), inline=True)
        msg.add_field(name = "Reliability", value = int(component_data["Reliability"]*component_data["Multiplier"]), inline=True)
        msg.add_field(name = "Pit Time", value = round(1-((1-component_data["Pit Time"])*component_data["Multiplier"]),ndigits=2), inline=True)
        msg.add_field(name = "TS", value = component_data["Power"]+component_data["Aero"]+component_data["Grip"]+component_data["Reliability"]+int(46-46*component_data["Pit Time"]), inline=True)
        msg.add_field(name = "PAG", value = int(component_data["Power"]*component_data["Multiplier"])+int(component_data["Aero"]*component_data["Multiplier"])+int(component_data["Grip"]*component_data["Multiplier"]), inline=True)
        msg.add_field(name = "PAGR", value = int(component_data["Power"]*component_data["Multiplier"])+int(component_data["Aero"]*component_data["Multiplier"])+int(component_data["Grip"]*component_data["Multiplier"])+int(component_data["Reliability"]*component_data["Multiplier"]), inline=True)
        msg.add_field(name = "Cards For Upgrade", value = component_data["Cards For Upgrade"], inline=False)
        msg.add_field(name = "Total Cards Needed", value = component_data["Total Cards Needed"], inline=False)
        msg.add_field(name = "Coins For Upgrade", value = "{:,}".format(component_data["Coins For Upgrade"]), inline=False)
        msg.add_field(name = "Total Coins Needed", value = "{:,}".format(component_data["Total Coins Needed"]), inline=False)
        msg.add_field(name = "Series", value = component_data["Series"], inline=False)
        await ctx.respond(embed = msg, ephemeral = True)
        print("Successfully replied to command")
    except Exception as e:
        print(e)
        print(component_data)
        await ctx.respond("An error has occured.", ephemeral = True)

@bot.slash_command(guild_ids=[963621040607600680], description = "Show Driver Stats")
async def comparedrivers(
    ctx: discord.ApplicationContext,
    driver1: Option(str, "Enter Driver Name", autocomplete = show_drivers, required = True),
    rarity1: Option(str, "Enter Driver Rarity", choices = ["Common", "Rare", "Epic"], required = True),
    level1: Option(int, "Enter Driver Level", choices = [i for i in range(1,12)], required = True),
    driver2: Option(str, "Enter Driver Name", autocomplete = show_drivers, required = True),
    rarity2: Option(str, "Enter Driver Rarity", choices = ["Common", "Rare", "Epic"], required = True),
    level2: Option(int, "Enter Driver Level", choices = [i for i in range(1,12)], required = True)
):
    try:
        print(driver1, rarity1, level1, driver2, rarity2, level2)
        driver_data_fields = ["Overtaking", "Defending", "Consistency", "Fuel Use", "Tyre Mgmt", "Wet Ability", "Max Quali", "Min Quali"]
        driver1_data = drivers.find_one({"Name": driver1, "Rarity": rarity1, "Level": level1})
        driver2_data = drivers.find_one({"Name": driver2, "Rarity": rarity2, "Level": level2})
        driver1_data["Max Quali"] = int(driver1_data["Overtaking"]*driver1_data["Multiplier"])+int(driver1_data["Defending"]*driver1_data["Multiplier"])+int(driver1_data["Fuel Use"]*driver1_data["Multiplier"])+int(driver1_data["Tyre Mgmt"]*driver1_data["Multiplier"])
        driver2_data["Max Quali"] = int(driver2_data["Overtaking"]*driver2_data["Multiplier"])+int(driver2_data["Defending"]*driver2_data["Multiplier"])+int(driver2_data["Fuel Use"]*driver2_data["Multiplier"])+int(driver2_data["Tyre Mgmt"]*driver1_data["Multiplier"])
        driver1_data["Min Quali"] = driver1_data["Max Quali"] - int(9930/(driver1_data["Consistency"]*driver1_data["Multiplier"])-103.74)
        driver2_data["Min Quali"] = driver2_data["Max Quali"] - int(9930/(driver2_data["Consistency"]*driver2_data["Multiplier"])-103.74)
        msg = discord.Embed(title = f"{level1} {rarity1} {driver1} | {level2} {rarity2} {driver2}", color = discord.Color.blurple())
        for field in driver_data_fields:
            if field != "Max Quali" and field != "Min Quali":
                driver1_data[field] = int(driver1_data[field]*driver1_data["Multiplier"])
                driver2_data[field] = int(driver2_data[field]*driver2_data["Multiplier"])
            msg.add_field(name = field, value = driver1_data[field], inline = True)
            msg.add_field(name = field, value = driver2_data[field], inline = True)
            if driver1_data[field] > driver2_data[field]:
                msg.add_field(name = "Difference", value = f"{driver1} ({round(driver1_data[field]-driver2_data[field], ndigits=2)})", inline = True)
            elif driver1_data[field] < driver2_data[field]:
                msg.add_field(name = "Difference", value = f"{driver2} ({round(driver2_data[field]-driver1_data[field],ndigits=2)})", inline = True)
            if driver1_data[field] == driver2_data[field]:
                msg.add_field(name = "Difference", value = f"EQUAL", inline = True)
    
        await ctx.respond(embed = msg, ephemeral = True)
        print("Successfully replied to command")
    except Exception as e:
        print(e)
        print(driver1_data, driver2_data)
        await ctx.respond("An error has occured.", ephemeral = True)



async def show_comps(ctx: discord.AutocompleteContext):
    comp_list = (['Starter Brake', 'Starter Gearbox', 'Starter RearWing', 'Starter FrontWing', 'Starter Suspension', 'Starter Engine', 'The Clog', 'The Steamroller', 'Q.T.3', 'The Striker', 'Harmony', 'The Blast', 'The Crunch', 'Orbit', 'The Crest', 'The Shadow', 'Titan', 'Temper', 'Tracer', 'Symbol', 'Blitz', 'The Method', 'The Phoenix', 'Quicksilver', 'ApeX', 'Spectre', 'The Strongbox', 'The Whirpool', 'Prestige', 'The Momentum', 'Mirage', 'The Renegade', 'The Prodigy', 'The Catalyst', 'Scorpion', 'Wild Boar', 'The Guerilla', 'The Jazz', 'Inferno 2.0', 'C.L.A.W.', 'Spirit', 'The Menace', 'The Vindicator', 'Hydra', 'Flow', 'True Grit', 'The Flux', 'Leviathan'])
    return([comp for comp in comp_list if ctx.value.lower().replace('.','') in comp.lower().replace('.','')])
@bot.slash_command(guild_ids=[963621040607600680], description = "Show Driver Stats")
async def compareparts(
    ctx: discord.ApplicationContext,
    comp1: Option(str, "Enter Component Name", autocomplete = show_comps, required = True),
    level1: Option(int, "Enter Component Level", choices = [i for i in range(1,12)], required = True),
    comp2: Option(str, "Enter Component Name", autocomplete = show_comps, required = True),
    level2: Option(int, "Enter Component Level", choices = [i for i in range(1,12)], required = True)
):
    try:
        print(comp1, level1, comp2, level2)
        comp_data_fields = ["Power", "Aero", "Grip", "Reliability", "Pit Time", "TS","PAG", "PAGR"]
        comp1_data = components.find_one({"Name": comp1, "Level": level1})
        comp2_data = components.find_one({"Name": comp2, "Level": level2})

        comp1_data["TS"] = comp1_data["Power"]+comp1_data["Aero"]+comp1_data["Grip"]+comp1_data["Reliability"]+int(46-46*comp1_data["Pit Time"])
        comp2_data["TS"] = comp2_data["Power"]+comp2_data["Aero"]+comp2_data["Grip"]+comp2_data["Reliability"]+int(46-46*comp2_data["Pit Time"])
        comp1_data["PAG"] = int(comp1_data["Power"]*comp1_data["Multiplier"])+int(comp1_data["Aero"]*comp1_data["Multiplier"])+int(comp1_data["Grip"]*comp1_data["Multiplier"])
        comp2_data["PAG"] = int(comp2_data["Power"]*comp2_data["Multiplier"])+int(comp2_data["Aero"]*comp2_data["Multiplier"])+int(comp2_data["Grip"]*comp2_data["Multiplier"])
        comp1_data["PAGR"] = int(comp1_data["Power"]*comp1_data["Multiplier"])+int(comp1_data["Aero"]*comp1_data["Multiplier"])+int(comp1_data["Grip"]*comp1_data["Multiplier"])+int(comp1_data["Aero"]*comp1_data["Multiplier"])
        comp2_data["PAGR"] = int(comp2_data["Power"]*comp2_data["Multiplier"])+int(comp2_data["Aero"]*comp2_data["Multiplier"])+int(comp2_data["Grip"]*comp2_data["Multiplier"])+int(comp2_data["Aero"]*comp1_data["Multiplier"])
        msg = discord.Embed(title = f"Level {level1} {comp1} | Level {level2} {comp2}", color = discord.Color.blurple())
        for field in comp_data_fields:
            msg.add_field(name = field, value = comp1_data[field], inline = True)
            msg.add_field(name = field, value = comp2_data[field], inline = True)
            comp1_data[field] = round(float(comp1_data[field]),ndigits=0)
            comp2_data[field] = round(float(comp2_data[field]),ndigits=0)
            if comp1_data[field] > comp2_data[field]:
                msg.add_field(name = "Difference", value = f"{comp1} ({round(comp1_data[field]-comp2_data[field],ndigits=2)})", inline = True)
            elif comp1_data[field] < comp2_data[field]:
                msg.add_field(name = "Difference", value = f"{comp2} ({round(comp2_data[field]-comp1_data[field],ndigits=2)})", inline = True)
            if comp1_data[field] == comp2_data[field]:
                msg.add_field(name = "Difference", value = f"EQUAL", inline = True)
    
        await ctx.respond(embed = msg, ephemeral = True)
        print("Successfully replied to command")
    except Exception as e:
        print(e)
        print(comp1_data, comp2_data)
        await ctx.respond("An error has occured.", ephemeral = True)



async def show_all(ctx: discord.AutocompleteContext):
    comp_list = (["Zhou","Magnussen","Latifi","Schumacher","Albon","Tsunoda","Stroll","Bottas","Ocon","Vettel","Ricciardo","Perez","Alonso","Gasly","Sainz","Leclerc","Russell","Norris","Verstappen","Hamilton",'Starter Brake', 'Starter Gearbox', 'Starter RearWing', 'Starter FrontWing', 'Starter Suspension', 'Starter Engine', 'The Clog', 'The Steamroller', 'Q.T.3', 'The Striker', 'Harmony', 'The Blast', 'The Crunch', 'Orbit', 'The Crest', 'The Shadow', 'Titan', 'Temper', 'Tracer', 'Symbol', 'Blitz', 'The Method', 'The Phoenix', 'Quicksilver', 'ApeX', 'Spectre', 'The Strongbox', 'The Whirpool', 'Prestige', 'The Momentum', 'Mirage', 'The Renegade', 'The Prodigy', 'The Catalyst', 'Scorpion', 'Wild Boar', 'The Guerilla', 'The Jazz', 'Inferno 2.0', 'C.L.A.W.', 'Spirit', 'The Menace', 'The Vindicator', 'Hydra', 'Flow', 'True Grit', 'The Flux', 'Leviathan'])
    return([comp for comp in comp_list if ctx.value.lower().replace('.','') in comp.lower().replace('.','')])
@bot.slash_command(guild_ids=[963621040607600680], description = "Boost a driver/comp")
async def boost(
    ctx: discord.AutocompleteContext,
    asset: Option(str, "Enter Asset to Boost", autocomplete=show_all,required = True),
    multiplier: Option(float, "Enter Multiplier", required = True)
):
    await ctx.defer()
    response = await ctx.respond("Updating multipliers...", ephemeral = True)
    if asset in drivers.distinct("Name"):
        for rarity in drivers.find({"Name": asset}).distinct("Rarity"):
            for level in drivers.find({"Name": asset, "Rarity": rarity}).distinct("Level"):
                drivers.find_one_and_update({"Name": asset, "Level": level, "Rarity": rarity},{"$set": {"Multiplier": float(multiplier)}})
                await response.edit(content=f"Level {level} {rarity} updated.")
        await ctx.respond(f"Updated {asset}'s multiplier to {multiplier}.", ephemeral = True)
    elif asset in components.distinct("Name"):
        for level in components.find({"Name": asset}).distinct("Level"):
            components.find_one_and_update({"Name": asset, "Level": level},{"$set": {"Multiplier": float(multiplier)}})
            await response.edit(content=f"Level {level} updated.")
        await ctx.respond(f"Updated {asset}'s multiplier to {multiplier}.", ephemeral = True)
    else:
        await ctx.respond("An error has occured.", ephemeral = True)
"""
@bot.slash_command(guild_ids=[877444044962275328,921918160058323034], description = "Find UUID of player with a certain IGN")
async def uuid(
    ctx: discord.ApplicationContext,
    ign: Option(str, "Enter IGN", required = True)
):
    request = requests.get("https://api.mojang.com/users/profiles/minecraft/" + ign).json()
    uuid = request['id']
    msg = discord.Embed(title = uuid, color = int('7FCC19',16))
    await ctx.respond(embed = msg)
"""


@bot.event
async def on_ready():
    print('Bot is online!')


bot.run(bot_token)
