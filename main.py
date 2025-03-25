
# imports for the start
import customtkinter as ctk  # pip install customtkinter
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageFont  # pip install Pillow
import pyglet, tkinter
import pandas as pd     # pip install pandas
import csv
import requests

# Class for the main menu
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Nicholas' Pokedex")
        self.geometry("850x300")
        ctk.set_appearance_mode("light")

        self.user = ""

        # title text
        self.image1 = Image.open("pokedexwelcome.png")
        self.tk_image1 = ImageTk.PhotoImage(self.image1)
        label1 = ctk.CTkLabel(self, text="", width=10, height=100, fg_color="transparent", image=self.tk_image1)
        label1.pack(pady=10)
        label1.place(relx=0.25, rely=0.075, anchor='w')

        # username entry
        self.user_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.user_entry.pack(pady=12, padx=10)
        self.user_entry.place(relx=0.43, rely=0.2)

        # password entry
        self.user_pass = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.user_pass.pack(pady=12, padx=10)
        self.user_pass.place(relx=0.43, rely=0.35)

        # button for login
        identify_button = ctk.CTkButton(self, text="Login", width=150, height=30, fg_color="#ee5351", command=self.loginsystem)
        identify_button.pack(pady=10)
        identify_button.place(relx=0.51, rely=0.527, anchor='center')

        # new user account button
        new_user_button = ctk.CTkButton(self, text="Create Account", width=75, height=7, fg_color="transparent", text_color='blue',font=("Pokemon GB", 9), command=self.account_creation_window)
        new_user_button.pack(pady=6)
        new_user_button.place(relx=0.42, rely=0.58)

        # function to check account details
    def checkdetails(self, accountpassword, checkaccountpassword ,account_name):
        if accountpassword.get() == checkaccountpassword.get():

            df = pd.read_csv('user_data.csv')
            accountusernames =  df["username"].values
            print(accountusernames)
            if account_name.get() in accountusernames:
                print("Username already in use")
                
            else:
                print("New username")

            
                new_account = pd.DataFrame([[account_name.get(), accountpassword.get() ,0,0,0,0,0,0]], columns=["username","password","pok1","pok2","pok3","pok4","pok5","pok6"])
                df = pd.concat([df, new_account], ignore_index=True)
                
                df.to_csv('user_data.csv', index=False)
                print(df)
                
                success_account_creation = ctk.CTkToplevel(self)
                success_account_creation.title("ACCOUNT CREATED")
                success_account_creation.geometry("400x70")

                accountcreation = ctk.CTkLabel(success_account_creation, text="Account successfully created", font=("Pokemon GB", 10),width=150,height=50)
                accountcreation.pack(pady=10, padx=10)
                accountcreation.place(relx=0.2, rely=0.25)
                
                success_account_creation.after(3000, success_account_creation.destroy)

        else:
            error_account_creation = ctk.CTkToplevel(self)
            error_account_creation.title("ERROR")
            error_account_creation.geometry("400x70")

            erroraccountcreation = ctk.CTkLabel(error_account_creation, text="Passwords do not match! Try again",font=("Pokemon GB", 10),width=150,height=50)
            erroraccountcreation.pack(pady=10, padx=10)
            erroraccountcreation.place(relx=0.1, rely=0.25)
            error_account_creation.after(3000, error_account_creation.destroy)

            

        # Account creation window
    def account_creation_window(self):
        account_creation = ctk.CTkToplevel(self)
        account_creation.title("Create Account")
        account_creation.geometry("300x300")
        account_creation.attributes("-topmost", 1)


        account_name = ctk.CTkEntry(account_creation, placeholder_text="Enter a username", fg_color='transparent', height= 50)
        account_name.pack(pady=10, padx=10)
        account_name.place(relx=0.28, rely=0.07)

        accountpassword = ctk.CTkEntry(account_creation, placeholder_text="Enter a Password", show="*", fg_color='transparent', height= 50)
        accountpassword.pack(pady=10, padx=10)
        accountpassword.place(relx=0.28, rely=0.25)

        checkaccountpassword = ctk.CTkEntry(account_creation, placeholder_text="Re-Enter your Password", show="*" , fg_color='transparent', height= 50)
        checkaccountpassword.pack(pady=10, padx=10)
        checkaccountpassword.place(relx=0.28, rely=0.45)

        account_creation_btn = ctk.CTkButton(account_creation,width=150, height=40, text="Create Account", command=lambda:[ self.checkdetails(accountpassword, checkaccountpassword, account_name), account_creation.destroy()])
        account_creation_btn.pack(pady=10, padx=10)
        account_creation_btn.place(relx=0.28, rely=0.65)
        
    def loginsystem(self):

        self.user = self.user_entry.get()
        passw = self.user_pass.get()


        df = pd.read_csv('user_data.csv')

        matching_creds = (len(df[(df.username == self.user) & (df.password == passw)]) > 0)
        
        if matching_creds:
            print('success')
            self.pokedex_menu()
        else:
            noaccount =ctk.CTkToplevel(self)
            noaccount.title("ERROR")
            noaccount.geometry('600x70')
            noaccount.attributes("-topmost",1)

            error_lbl = ctk.CTkLabel(noaccount,text="Your Account is not registered or details are incorrect",font=("Pokemon GB",10))
            error_lbl.pack(pady=10)
            error_lbl.place(relx=0.02,rely=0.1)

            tryagain_lbl = ctk.CTkLabel(noaccount,text="Please try again",font=("Pokemon GB",10))
            tryagain_lbl.pack(pady=5)
            tryagain_lbl.place (relx=0.35,rely=0.5)
            noaccount.after(4000, noaccount.destroy)




        # command to open a pokedex window
    def pokedex_menu(self):
        

        # Create a new top-level window
        new_window = ctk.CTkToplevel(self)
        new_window.title("Pokedex")
        new_window.geometry('700x500')

        #  Make the window open on top of the other menu
        new_window.attributes("-topmost", 1)

        # hides the login menu
        self.withdraw()

        # shows the teams (from the csv)
        team_lbl = ctk.CTkLabel (new_window, text="Team", width=150 , height= 30,font=("Pokemon GB",20), fg_color='#3b8ed0')
        team_lbl.pack(pady=10)
        team_lbl.place(relx=0.45, rely=0.3)

        #user name
        df = pd.read_csv('user_data.csv')
        usernamelabel= ctk.CTkLabel (new_window,text=self.user_entry.get(),width=170,height=50,fg_color="crimson",font=("Pokemon GB", 15))
        usernamelabel.pack(pady=10)
        usernamelabel.place(relx=0.214)

        #search button

        searchlabel = ctk.CTkLabel (new_window,text="Search",width=150,height=30,fg_color="transparent",text_color='black' , font=("Pokemon GB", 15))
        searchlabel.pack(pady=10)
        searchlabel.place(relx=0.7)

        #search button
        self.image3 = Image.open('fixedsearch.png')
        self.tk_image3 = ImageTk.PhotoImage(self.image3)
        searchbtn = ctk.CTkButton(new_window,text='', width=25 , height= 25, image=self.tk_image3,fg_color='transparent',command=lambda: self.close_and_run_search(new_window)  )
        searchbtn.pack(pady=10)
        searchbtn.place(relx=0.9)

    


        #settings button
        self.settingbtn = Image.open('setting2.png')
        self.tk_settingbtn = ImageTk.PhotoImage(self.settingbtn)
        settingbtn = ctk.CTkButton(new_window,text='',image=self.tk_settingbtn,fg_color='transparent',width=30,height=30, command=self.settings_window)
        settingbtn.pack(pady=10)
        settingbtn.place(relx=0.01,rely=0.87)



        # import the csv 

        df = pd.read_csv('user_data.csv')
        print(df)
        # after reading the csv, it only reads the row that belongs to said user.
        user_data = df[df['username'] == self.user].iloc[0]
        print(df[df['username'] == self.user])
        pokemons = user_data[['pok1', 'pok2', 'pok3', 'pok4', 'pok5', 'pok6']].values
        

        self.create_pokemon_buttons(new_window, pokemons)

    def close_and_run_search(self, current_window):
        # Close the current window
        current_window.destroy()  # This will close the `new_window` when the search button is clicked
        
        # Run the search window command
        self.search_window()  # This assumes `search




        # makes the buttons to place in the pokedex menu to show the teams
    def create_pokemon_buttons(self, new_window, pokemons):
    
        rows = 2
        cols = 3

        for i, pokemon_id in enumerate(pokemons):
            self.create_pokemon_button(new_window, pokemon_id, i + 1, rows, cols)

        # imports the api and loads the sprites
    def create_pokemon_button(self, new_window, pokemon_id, button_num, rows, cols):
        try:
            url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
            response = requests.get(url, stream=True)

            if response.status_code == 200:
                image = Image.open(response.raw)
                image = image.resize((64, 64))  
                sprite = ImageTk.PhotoImage(image)
            else:
                sprite = None
                print(f"Error loading sprite for Pokémon ID {pokemon_id}")

        
            rows = (button_num - 1) // cols  
            col = (button_num - 1) % cols   

            # Grid positions at the bottom-right corner of the window
            base_x = 0.23  
            base_y = 0.42  
            x_spacing = 0.30  
            y_spacing = 0.25  

            x_pos = base_x + (col * x_spacing)
            y_pos = base_y + (rows * y_spacing)

            # button for the sprites
            poke_button = ctk.CTkButton(new_window, text=f"Pokemon {button_num}", image=sprite, compound="top", width=100, height=100,command=lambda pokemon_id=pokemon_id: self.show_pokemon_details(pokemon_id) )
            poke_button.image = sprite  
            poke_button.pack(padx=10)
            poke_button.place(relx=x_pos, rely=y_pos)

        except Exception as e:
            print(f"Error loading sprite for Pokémon ID {pokemon_id}: {e}")


    



        # function to open the settings menu
    def settings_window(self):

        settings_window = ctk.CTkToplevel(self)
        settings_window.title("SETTINGS")
        settings_window.geometry('300x100')
        settings_window.attributes("-topmost", 1)


        editname_lbl = ctk.CTkLabel(settings_window,text="Edit Name", font=("Pokemon GB",10))
        editname_lbl.pack(pady=10)
        editname_lbl.place(relx=0.04,rely=0.05)

        editname_ent = ctk.CTkEntry(settings_window,placeholder_text="Enter new name",font=("Pokemon GB",10))
        editname_ent.pack(pady=10)
        editname_ent.place(relx=0.35,rely=0.05)

        saveeditname_btn = ctk.CTkButton(settings_window,text="save",width=20,font=("Pokemon GB",10),command=lambda: self.save_new_username(editname_ent.get()))
        saveeditname_btn.pack(pady=10)
        saveeditname_btn.place(relx=0.82,rely=0.05)

    

        deleteaccount_lbl = ctk.CTkLabel(settings_window,text="Delete Account",font=("Pokemon GB",10))
        deleteaccount_lbl.pack(pady=10)
        deleteaccount_lbl.place(relx=0.04,rely=0.4)

        deleteaccount_btn = ctk.CTkButton(settings_window,text="DELETE",command=self.confirmaccountdelete,font=("Pokemon GB",10))
        deleteaccount_btn.pack(pady=10)
        deleteaccount_btn.place(relx=0.52,rely=0.4)

    


    def save_new_username(self, new_username):
        if new_username.strip() == "":
            print("Username cannot be empty.")
            return

        # Read the CSV file
        df = pd.read_csv('user_data.csv')

        if new_username in df['username'].values:
            print("This username is already taken. Please choose a different one.")
            return

        # Update the username for the current user
        df.loc[df['username'] == self.user, 'username'] = new_username

        # Save the updated DataFrame back to CSV
        df.to_csv('user_data.csv', index=False)

        # Update the username in memory as well
        self.user = new_username
        print(f"Username updated to {self.user}")
        

    def confirmaccountdelete(self):
        confirmaccountdelete=ctk.CTkToplevel(self)
        confirmaccountdelete.title("Confirm Account Delete")
        confirmaccountdelete.geometry("200x100")
        confirmaccountdelete.attributes("-topmost", 1)

        confirmbutton = ctk.CTkButton (confirmaccountdelete,text="CONFIRM",font=("Pokemon GB",15),command=self.account_deleted)
        confirmbutton.pack()
        confirmbutton.place(relx=0.15,rely=0.3)


    def account_deleted(self):
        df = pd.read_csv('user_data.csv')
        user_data = df[df['username'] == self.user]
        user_index = user_data.index[0]

        # removes the user from the dataframe
        df.drop(user_index, inplace=True)

        # saves the updated dataframe back to the CSV file
        df.to_csv('user_data.csv', index=False)

        print(f"Account for {self.user} has been deleted.") # for debugging
        
    


        # funtion to open the search window/menu
    def search_window(self):
        


        self.current_page = 0 
        self.pokemon_images = [] 


        search_window = ctk.CTkToplevel(self)
        search_window.title("SEARCH")
        search_window.geometry('800x600')
        search_window.attributes("-topmost", 1)
        
        searchentry = ctk.CTkEntry (search_window,placeholder_text="Search by Name or Number",width=400,height=30,text_color='black' , font=("Pokemon GB", 15))
        searchentry.pack(pady=5)
        searchentry.place(relx=0.26,rely=0.03,)
        submitbtn =ctk.CTkButton (search_window,text="ENTER", command=lambda:self.search_pokemon(searchentry)) 
        submitbtn.pack(pady=5)
        submitbtn.place(relx=0.6,rely=0.09)

        returnmenubtn = ctk.CTkButton(search_window,text="Return to Pokedex Menu",font=("Pokemon GB", 7), command=self.pokedex_menu)
        returnmenubtn.pack(pady=10)
        returnmenubtn.place(relx = 0.18 , rely = 0.09 )

        nextpagebtn = ctk.CTkButton(search_window, text="---->",command=lambda:self.change_page(1, search_window)) # I DONT KNOW WHY THIS BUTTON DOES NOT WANT TO APPEAR
        nextpagebtn.pack(pady=10)
        nextpagebtn.place(relx= 0.8 , rely = 0.03,sticky='e')

        previouspagebtn = ctk.CTkButton(search_window,text="<----",command= lambda:self.change_page(-1 , search_window)) # I DONT KNOW WHY THIS BUTTON DOES NOT WANT TO APPEAR
        previouspagebtn.pack(pady=10)
        previouspagebtn.place(relx=0.3, rely= 0.06, )


        returnmenubtn = ctk.CTkButton(search_window,text="Return to Pokedex Menu",font=("Pokemon GB", 7))
        returnmenubtn.pack(pady=10)
        returnmenubtn.place(relx = 0.18 , rely = 0.04 )



        self.load_pokemon_images(search_window)

    def load_pokemon_images(self, search_window):
        # Clear previously loaded buttons and images
            for widget in search_window.winfo_children():
                if isinstance(widget, ctk.CTkButton) and widget not in [search_window.winfo_children()[0], search_window.winfo_children()[1], search_window.winfo_children()[2]]:
                    widget.destroy()
            
            start_id = self.current_page * 12 + 1  
            self.pokemon_images = []  

            for i in range(12):  
                pokemon_id = start_id + i 

                try:
                    # gets the sprite from the API
                    url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_id}.png"
                    response = requests.get(url, stream=True)
                    if response.status_code == 200:
                        image = Image.open(response.raw)
                        image = image.resize((100, 100))  
                        sprite = ImageTk.PhotoImage(image)
                        self.pokemon_images.append(sprite)  
                    else:
                        sprite = None
                except Exception as e:
                    print(f"Error loading sprite for Pokémon {pokemon_id}: {e}")
                    sprite = None

                xposition = 0.1 + ((i % 4)) * 0.225
                yposition = 0.22 + (i // 4) * 0.25

                # create the button that displays the pokemon front facing sprite
                poke_button = ctk.CTkButton(search_window, text=f' {pokemon_id} ', image=sprite, compound="top", width=100, height=100,command=lambda pokemon_id=pokemon_id: self.show_pokemon_details(pokemon_id))
                poke_button.pack(pady=10)
                poke_button.place(relx=xposition, rely=yposition)  

    


        # function to change the page for pokemon (doesnt seem to want to show the previous page btn)
    def change_page(self, direction, search_window):

        self.current_page += direction


        if self.current_page < 0:
            self.current_page = 0


        self.load_pokemon_images(search_window)
        
        # shows all the details of the pokemon searched or clicked
    def show_pokemon_details(self, pokemon_id):
        details_window = ctk.CTkToplevel(self)
        details_window.title(f"Pokémon #{pokemon_id} Details")
        details_window.geometry("400x500")
        details_window.attributes("-topmost", 1)

        try:
            
            url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                name = data["name"].capitalize()
                height = data["height"] / 10  
                weight = data["weight"] / 10  
                types = ", ".join(t["type"]["name"].capitalize() for t in data["types"])

                # Get the Pokémon sprite
                sprite_url = data["sprites"]["front_default"]
                sprite_response = requests.get(sprite_url, stream=True)
                if sprite_response.status_code == 200:
                    sprite_image = Image.open(sprite_response.raw)
                    sprite_image = sprite_image.resize((150, 150))
                    sprite_photo = ImageTk.PhotoImage(sprite_image)
                else:
                    sprite_photo = None
            else:
                name, height, weight, types, sprite_photo = "Unknown", "?", "?", "?", None

        except Exception as e:
            print(f"Error fetching Pokémon details: {e}")
            name, height, weight, types, sprite_photo = "Unknown", "?", "?", "?", None

        
        if sprite_photo:
            sprite_label = ctk.CTkLabel(details_window, image=sprite_photo, text="")
            sprite_label.image = sprite_photo  
            sprite_label.pack(pady=10)

        # Display Pokémon Details

        details_text = f"Name: {name}\nHeight: {height} m\nWeight: {weight} kg\nType(s): {types}"
        details_label = ctk.CTkLabel(details_window, text=details_text, font=("Pokemon GB", 15))
        details_label.pack(pady=10)

        # the button that will allow you to add the pokemon to the team

        add_to_team_button = ctk.CTkButton(details_window,text="Add to Team", width=100,height=75,command= lambda: self.addtoteam(pokemon_id))
        add_to_team_button.pack(pady=10)
        add_to_team_button.place(relx = 0.35 , rely=0.6)

    def addtoteam(self,pokemon_id):
        
        # reads the csv and selects the login user 
        df = pd.read_csv('user_data.csv')
        user_data = df[df['username'] == self.user].iloc[0]
        current_pokemon_party = user_data[['pok1', 'pok2', 'pok3', 'pok4', 'pok5', 'pok6']].values.tolist()


        # checks if there is an empty slot in the party
        empty_slot = next((i for i, poke in enumerate(current_pokemon_party) if poke == ""), None)


            # if there is an empty slot it will add the pokemon to the first slot
        if empty_slot is not None:
            # if space available, add the Pokémon to the first empty slot
            current_pokemon_party[empty_slot] = pokemon_id
            action = "added"
        else:
            # team is full, ask user which Pokémon to swap
            action = "swapped"
        
        # creates a new window which will allow the the user to swap pokemon
        swap_window = ctk.CTkToplevel(self)
        swap_window.title(f"Swap Pokémon for #{pokemon_id}")
        swap_window.geometry("450x400")
        
        prompt_label = ctk.CTkLabel(swap_window, text="Choose which slot to add the pokemon too", font=("Pokemon GB", 9))
        prompt_label.pack(pady=10)
        
        # Display the Pokémon currently in the team with buttons to swap
        for i, poke_id in enumerate(current_pokemon_party):
            poke_button = ctk.CTkButton(swap_window, text=f"Pokémon #{poke_id}", width=200, height=50,command=lambda poke_id=poke_id, index=i: self.swap_pokemon(pokemon_id, poke_id, index, current_pokemon_party, df, swap_window))
            poke_button.pack(pady=5)



        # If action is not "swapped", save the changes to the CSV
        if action != "swapped":
            # Update the team in the dataframe
            df.loc[df['username'] == self.user, ['pok1', 'pok2', 'pok3', 'pok4', 'pok5', 'pok6']] = current_pokemon_party
            # Save the updated dataframe back to the CSV file
            df.to_csv('user_data.csv', index=False)
            print(f"Pokémon #{pokemon_id} has been {action} to the team!") # for debugging
        
    def swap_pokemon(self, new_pokemon_id, old_pokemon_id, swap_index, current_team, df, swap_window):
        
        current_team[swap_index] = new_pokemon_id
        
        swap_window.destroy()
        
        
        df.loc[df['username'] == self.user, ['pok1', 'pok2', 'pok3', 'pok4', 'pok5', 'pok6']] = current_team
        
        # Save the updated dataframe back to the CSV file
        df.to_csv('user_data.csv', index=False)
        print(f"Pokémon #{old_pokemon_id} has been swapped with Pokémon #{new_pokemon_id}.") # for debugging


        # function to check what pokemon name or id is typed in or button clicked
    def search_pokemon(self, search_entry):
        pokemon_name_or_id = search_entry.get().lower()  
        if not pokemon_name_or_id:
            return  

        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            pokemon_name = data["name"].capitalize()
            pokemon_id = data["id"]
            pokemon_sprite = data["sprites"]["front_default"]
            pokemon_types = [t["type"]["name"].capitalize() for t in data["types"]]

        
            self.display_pokemon_results(pokemon_name, pokemon_id, pokemon_sprite, pokemon_types)

        else:
            print("Pokemon not found!")


        # after the search
    def display_pokemon_results(self, name, id, sprite, types):
        
        results_window = ctk.CTkToplevel(self)
        results_window.title(name)
        results_window.geometry("400x400")

        name_label = ctk.CTkLabel(results_window, text=f"Name: {name}")
        name_label.pack(pady=10)

        id_label = ctk.CTkLabel(results_window, text=f"ID: {id}")
        id_label.pack(pady=10)

        type_label = ctk.CTkLabel(results_window, text=f"Type: {', '.join(types)}")
        type_label.pack(pady=10)

        

    
        response = requests.get(sprite, stream=True)
        img = Image.open(response.raw)
        img = img.resize((100, 100))
        img = ImageTk.PhotoImage(img)

        image_label = ctk.CTkLabel(results_window, image=img, text="")
        image_label.image = img  
        image_label.pack(pady=10)


    






# Initialize and run the app

app = App()
app.mainloop()
