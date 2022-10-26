import discord
import math
from discord.commands import Option
from discord.ui import Button, View
import json
import time
from driver_stats.DriverStats import fetchDriverStats
from component_stats.ComponentStats import fetchCompStats
from race_debrief.write_to_csv import write_race_debrief
import os


bot = discord.Bot()
invite_link = "https://discord.com/api/oauth2/authorize?client_id=1011606897729732708&permissions=517543840832&scope=bot"
bot_token = "MTAxMTYwNjg5NzcyOTczMjcwOA.GRfWAV.VKJwtGKFwqrQPYTlN8KpvuQp8pWr0rL8NMwZ8E"
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
        driver_data = fetchDriverStats(driver, rarity, level, boostedDrivers, boostedComps)
        msg = discord.Embed(title = f"Level {level} {rarity} {driver}", color = discord.Color.blurple())
        for field in driver_data:
            msg.add_field(name = field, value = driver_data[field], inline = True)
    
        await ctx.respond(embed = msg, ephemeral = True)
        print("Successfully replied to command")
    except Exception as e:
        print(e)
        print(driver_data)
        await ctx.respond("An error has occured.", ephemeral = True)

async def seriesoptions(ctx: discord.AutocompleteContext):
    options = ["1","2","3","4","5","6","7","8","9","10","11","12","Junior OR","Junior FR","Challenger OR","Challenger FR","Contender OR","Contender FR","Champion OR","Champion FR"]
    return([o for o in options if ctx.value.lower() in o.lower()])
@bot.slash_command(guild_ids=[963621040607600680], description = "Show Driver Stats")
async def debrief(
    ctx: discord.ApplicationContext,
    series: Option(str, "Enter Series", autocomplete = seriesoptions,required = True),
    track: Option(str, "Enter Track Name", required = True),
    data: Option(str, "Enter Debrief Data", required = True)
):
    msg = write_race_debrief(series, track, data)
    try:
        await ctx.respond(f"```\n{msg}```", ephemeral = True)
    except Exception as e:
        print(e)
        print(track)
        print(data)
        await ctx.respond(f"An error has occured. This was your entered data.\n```\nTrack Name: {track}\nData: {data}", ephemeral = True)


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
        driver_data_fields = ["Overtaking", "Defending", "Consistency", "Fuel Use", "Tyre Mgmt", "Wet Ability", "Total Value", "Dry Quali"]
        driver1_data = fetchDriverStats(driver1, rarity1, level1, boostedDrivers, boostedComps)
        driver2_data = fetchDriverStats(driver2, rarity2, level2, boostedDrivers, boostedComps)
        msg = discord.Embed(title = f"{level1} {rarity1} {driver1} | {level2} {rarity2} {driver2}", color = discord.Color.blurple())
        for field in driver_data_fields:
            msg.add_field(name = field, value = driver1_data[field], inline = True)
            msg.add_field(name = field, value = driver2_data[field], inline = True)
            driver1_data[field] = int(driver1_data[field])
            driver2_data[field] = int(driver2_data[field])
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
        comp_data_fields = ["Power", "Aero", "Grip", "Reliability", "Pit Time", "Total", "Team Score"]
        comp1_data = fetchCompStats(comp1, level1, boostedDrivers, boostedComps)
        comp2_data = fetchCompStats(comp2, level2, boostedDrivers, boostedComps)
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




@bot.slash_command(guild_ids=[963621040607600680], description = "Boost a driver/comp")
async def boost(
    ctx: discord.AutocompleteContext,
    change: Option(bool, "Add or remove", required = True),
    driver: Option(str, "Enter Driver", autocomplete=show_drivers,required = False),
    comp: Option(str, "Enter Component", autocomplete=show_comps, required = False)
):
    global boostedComps, boostedDrivers
    if driver != None:
        if driver not in boostedDrivers:
            if change:
                try:
                    boostedDrivers.append(driver)
                    await ctx.respond(f"{driver} added to boosted list.", ephemeral=True)
                except Exception as e:
                    await ctx.respond(e, ephemeral=True)
            else:
                try:
                    boostedDrivers.remove(driver)
                    await ctx.respond(f"{driver} removed from boosted list.", ephemeral=True)
                except Exception as e:
                    await ctx.respond(e, ephemeral=True)
    if comp != None:
        if comp not in boostedDrivers:
            if change:
                try:
                    boostedComps.append(comp)
                    await ctx.respond(f"{comp} added to boosted list.", ephemeral=True)
                except Exception as e:
                    await ctx.respond(e, ephemeral=True)
            else:
                try:
                    boostedComps.remove(comp)
                    await ctx.respond(f"{comp} removed from boosted list.", ephemeral=True)
                except Exception as e:
                    await ctx.respond(e, ephemeral=True)
                
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
