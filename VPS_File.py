import discord
from discord.ui import Button
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import time
from datetime import datetime
import os
 
import gspread
from oauth2client.service_account import ServiceAccountCredentials
load_dotenv()
 
intents = discord.Intents().all()
bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
TOKEN = 'TOKENED'
drivers = ['ALB','ALO','BOT','DEV','GAS','HAM','HUL','LEC','MAG','NOR','OCO','PER','PIA','RUS','SAI','SAR','STR','TSU','VER','ZHO']
drivers_fullname = ['Alexander Albon', 'Fernando Alonso', 'Valtteri Bottas', 'Nyck de Vries', 'Pierre Gasly', 'Lewis Hamilton', 'Nico Hülkenberg', 'Charles Leclerc', 'Kevin Magnussen', 'Lando Norris', 'Esteban Ocon', 'Sergio Pérez', 'Oscar Piastri', 'George Russell', 'Carlos Sainz', 'Logan Sargeant', 'Lance Stroll', 'Yuki Tsunoda', 'Max Verstappen', 'Zhou Guanyu']
tipp_to_file = ''
mod_roles = [441267211177426944, 794688356491067412, 794812802144927785]
 
@bot.event
async def on_ready():
    print('bot elindult')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
    except Exception as e:
        print(f'Error: {e}')
 
@bot.tree.command(name='tippem')
@app_commands.describe(első = 'Első helyezett', második = 'második helyezett', harmadik = 'harmadik helyezett')
async def tippem(interaction: discord.integrations, első: str, második: str, harmadik: str):
    global tipp_to_file
    await interaction.response.defer()
    with open('enddate.txt', 'r') as read_enddate:
            now = datetime.now()
            enddate_str = '2023.'+str(read_enddate.readline().replace('\n', ''))
            enddate_date = datetime.strptime(enddate_str, '%Y.%m.%d %H')
 
            if now < enddate_date:
                if első in drivers and második in drivers and harmadik  in drivers:
                    tipp = '1: ' + első + '\n2: ' + második + '\n3: ' + harmadik
                    tipp_to_file = tipp
                    button_Accept = Button(label="Tipp megerősítése", style=discord.ButtonStyle.green, custom_id="guess_accepted" + str(interaction.user.id))
                    button_Cancel = Button(label="Mégse", style=discord.ButtonStyle.red, custom_id="guess_cancelled")
                    view = discord.ui.View(timeout=None)
                    view.add_item(button_Accept)
                    view.add_item(button_Cancel)
                    embed = discord.Embed(
                        title = str(interaction.user.name) + " Tippje",
                        description = 'Nyomj a "Tipp megerősítésre" ha ezt a tippet szeretnéd leadni: \n\n' + tipp + '\nHa változtatni szerenél nyomj a "Mégse" gombra és add le újra a tipped.',
                        color=0xF55742
                        )
                    embed.set_footer(text='Crappa Discord - F1 Tippverseny')
                    await interaction.channel.send(embed=embed, view=view)
                else:
                    view = discord.ui.View(timeout=None)
                    embed = discord.Embed(
                        title = 'HIBA!!!',
                        description = 'Hibásan adtad le a tippet. Valamelyik pilóta nevét helytelenül írtad le, esetleg a szintaktikai hibát ejtettél. Segítségért írd be a következő parancsot: $drivers',
                        color=0xF55742
                        )
                    embed.set_footer(text='Crappa Discord - F1 Tippverseny')
                    await interaction.channel.send(embed=embed, view=view)
            else:
                view = discord.ui.View(timeout=None)
                embed = discord.Embed(
                    title = 'Lejárt az idő',
                    description = 'A mostani versenyre már nincs lehetőséged szavazni!',
                    color=0xF55742
                    )
                embed.set_footer(text='Crappa Discord - F1 Tippverseny')
                await interaction.channel.send(embed=embed, view=view)
 
@bot.tree.command(name='winner')
@app_commands.describe(winner_első = 'Első hely', winner_második = 'második hely', winner_harmadik = 'harmadik hely')
async def tippem(interaction: discord.integrations, winner_első: str, winner_második: str, winner_harmadik: str):
    mod_roles = [1086785649975242842]
    member_role = []
    for role in interaction.user.roles:
        member_role.append(role.id)
    if any(role in member_role for role in mod_roles): 
        with open('enddate.txt', 'r+') as read_enddate:
            now = datetime.now()
            enddate_str = '2023.'+str(read_enddate.readline().replace('\n', ''))
            enddate_date = datetime.strptime(enddate_str, '%Y.%m.%d %H')
 
            if 1 == 1:    
                print('Nyertesek kihirdetve')
 
                folder_path = "/home/container/Tippek"
                file_list = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
 
                row_value = []
                already_checked = []
                username_list = []
                for file in file_list:
                    point_to_win = 0
                    tipp_list = []
                    line_count = 0
                    with open(os.path.join(folder_path, file), "r") as f:
                        for line in f:
                            if line_count < 3:
                                line = line[3:]
                                line = line[:3]
                                tipp_list.append(line)
                                line_count +=1
                    file_name_to_user = file.replace('.txt', '')
                    user_name_from_file = bot.get_user(int(file_name_to_user))   
 
 
                    if tipp_list[0] == winner_első:
                        point_to_win = point_to_win + 25
                    if tipp_list[1] == winner_második:
                        point_to_win = point_to_win + 18
                    if tipp_list[2] == winner_harmadik:
                        point_to_win = point_to_win + 15
 
                    username_list.append(user_name_from_file.name + 'POINT_TO_WIN=' + str(point_to_win))  
 
                scopes = [
                    'https://www.googleapis.com/auth/spreadsheets',
                    'https://www.googleapis.com/auth/drive'
                ]
                creds = ServiceAccountCredentials.from_json_keyfile_name('secret_key.json', scopes=scopes)
 
                file = gspread.authorize(creds)
                workbook = file.open('Crappa 2023 F1 tippverseny')
                sheet = workbook.worksheet("Tippverseny")
 
                with open("enddate.txt", "r") as f:
                    line_count = len(f.readlines())
                x = 1
                y = 23
                y = y - line_count
 
                for row in sheet.col_values(1):
                    if row not in row_value and row != 'Versenyek:':
                        row_value.append(row + 'XPLACE=' + str(x))
 
                    x +=1
                    if row == user_name_from_file.name and row not in already_checked:       
                        #print(user_name_from_file.name)
                        already_checked.append(str(user_name_from_file.name))
 
                # végigmegyünk a username listán
                for name in username_list:
                    # kinyerjük a név és a POINT_TO_WIN értéket
                    name_parts = name.split("POINT_TO_WIN=")
                    name_only = name_parts[0]
                    point_to_win = name_parts[1]
 
                    # ellenőrizzük, hogy a nevünk szerepel-e az XPLACE értékekkel ellátott sheets_list listában
                    for rows in row_value:
                        if name_only in rows:
                            # ha igen, akkor kinyerjük az XPLACE értéket
                            x_place = rows.split("XPLACE=")[1]
                            x_place_value = int(x_place)
                            print(f"{name_only}: XPLACE={x_place_value}, POINT_TO_WIN={point_to_win}")
                            point_to_win = str(point_to_win)
                            #sheet.update_cell(x_place_value, y+2, point_to_win)
 
                with open("enddate.txt", "r") as file:
                    lines = file.readlines()
                    del lines[0]  # első sor törlése
 
                with open("enddate.txt", "w") as file:
                    file.writelines(lines)
 
            else:
                view = discord.ui.View(timeout=None)
                embed = discord.Embed(
                    title = 'HIBA!!!',
                    description = 'Még nem zárhatod le a versenyt hiszen még el se kezdődött.',
                    color=0xF55742
                    )
                embed.set_footer(text='Crappa Discord - F1 Tippverseny')
                await interaction.channel.send(embed=embed, view=view)
 
@bot.event
async def on_message(message):
    global tipp_to_file  
 
    if message.content == '$help':
        if message.channel.id == 1083834533725601894:
            view = discord.ui.View(timeout=None)
            embed = discord.Embed(
                title = 'Segítség',
                description = 'Az alábbi parancsok lehetnek a segítségedre:\n$drivers - Versenyzők nevei.\n$tippem - Saját tipped megnézése.',
                color=0xF55742
                )
            embed.set_footer(text='Crappa Discord - F1 Tippverseny')
            await message.channel.send(embed=embed, view=view)
 
    if message.content == '$drivers':
        drivers_message = ''
        for i in range(0, len(drivers)):
            drivers_message = drivers_message + drivers[i] + ' - ' + drivers_fullname[i] + '\n'
        if message.channel.id == 1083834533725601894:
            view = discord.ui.View(timeout=None)
            embed = discord.Embed(
                title = 'Pilóták',
                description = 'Az alábbi 3 betűs rövidített neveket írd be a tippedbe:\n' + drivers_message,
                color=0xF55742
                )
            embed.set_footer(text='Crappa Discord - F1 Tippverseny')
            await message.channel.send(embed=embed, view=view)
 
    if message.content == '$tippem':
        read_tipp = []
        tipp_message = ''
        try:
            with open('/home/container/Tippek/' + str(message.author.id) + '.txt', 'r') as command_tipp:
                for line in command_tipp:
                    read_tipp.append(line)
                for i in range(len(read_tipp)):
                    read_tipp[i] = read_tipp[i][3:].replace('\n', '')
                tipp_message = '1: ' + read_tipp[0] + '\n2: ' + read_tipp[1] + '\n3: ' + read_tipp[2]
 
                view = discord.ui.View(timeout=None)
                embed = discord.Embed(
                    title = str(message.author) + ' tipped', #nem tudom ide valamit kéne írni mert bánatul néz ki
                    description = 'A tipped jelenleg a következő:\n' + tipp_message + '\nHa új tippet szeretnél leadni akkor ugyan úgy mint eddig, add le újra a tippet.',
                    color=0xF55742
                    )
                embed.set_footer(text='Crappa Discord - F1 Tippverseny')
                await message.channel.send(embed=embed, view=view)
        except:
            view = discord.ui.View(timeout=None)
            embed = discord.Embed(
                title = 'HIBA!!!',
                description = 'Nincsen aktuális tipped leadva. Segítségért írd be, hogy $help',
                color=0xF55742
                )
            embed.set_footer(text='Crappa Discord - F1 Tippverseny')
            await message.channel.send(embed=embed, view=view)
 
    if message.content == '$tesztelek':
        read_tipp = []
        tipp_message = ''
        with open('/home/container/Tippek/' + str(message.author.id) + '.txt', 'r') as command_tipp:
            for line in command_tipp:
                read_tipp.append(line)
            for i in range(len(read_tipp)):
                read_tipp[i] = read_tipp[i][3:].replace('\n', '')
            tipp_message = '1: ' + read_tipp[0] + '\n2: ' + read_tipp[1] + '\n3: ' + read_tipp[2]
            print (tipp_message)
 
    if message.content == '$enddate':
        enddate_settings = []
        with open('enddate.txt', 'r') as read_enddate:
            first_line = read_enddate.readline()
            enddate_settings.append(first_line)
        await message.channel.send('Eddig tudsz szavazni: 2023.' + enddate_settings[0].replace('\n', '') + ':00')
        enddate_settings.clear()
 
@bot.event
async def on_interaction(interaction):
     global tipp_to_file
     if isinstance(interaction, discord.Interaction) and interaction.type == discord.InteractionType.component:
        custom_id_checker = 'guess_accepted' + str(interaction.user.id)
        if interaction.data.get("custom_id") == custom_id_checker:
            await interaction.response.defer()
            await interaction.channel.purge(limit=1)
            await interaction.channel.send(str(interaction.user.mention) + ' sikeresen leadtad a tipped.')
            with open('/home/container/Tippek/' + str(interaction.user.id) + '.txt', 'a') as new_tipp:
                print('new_tipp')
            with open('/home/container/Tippek/' + str(interaction.user.id) + '.txt', 'w') as new_tipp:
                new_tipp.write(tipp_to_file)
            new_tipp.close()
 
            #Excel tábla írása
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_name('secret_key.json', scopes=scopes)
 
            file = gspread.authorize(creds)
            workbook = file.open('Crappa 2023 F1 tippverseny')
            sheet = workbook.worksheet("Tippverseny")
            a_col = sheet.col_values(1)
            value_count = 1
            tippers = []
            for value in a_col:
                tippers.append(value)
                if value != '':
                    value_count +=1
            if interaction.user.name not in tippers:
                print('A'+str(value_count))
                sheet.update_acell('A'+str(value_count), interaction.user.name)
            tippers.clear()
 
        else:
            await interaction.response.defer()
            await interaction.channel.purge(limit=2)
            await interaction.channel.send(str(interaction.user.mention) + ' a tipped visszavonva.')
            time.sleep(10)
            await interaction.channel.purge(limit=1)
 
bot.run(TOKEN)