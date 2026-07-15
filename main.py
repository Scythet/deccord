import flet as ft
import subprocess
import random
import string

DB = {
    "users": {
        "admin@acc.com": {
            "email": "admin@acc.com",
            "password": "admin",
            "username": "admin",
            "display_name": "ACC Administrator",
            "phone": "+34600000000",
            "bio": "Anti Chat Control Developer.",
            "avatar": "https://i.postimg.cc/85zX7f00/logo-shield.png",
            "banner": "#1a237e",
            "status": "Online",
            "status_color": ft.Colors.GREEN_400,
            "dev_mode": True,
            "read_receipts": True,
            "friends": ["pedro", "sofia"]
        }
    },
    "groups": [
        {
            "name": "ACC Main Lounge",
            "photo": "https://i.postimg.cc/85zX7f00/logo-shield.png",
            "invitations": ["antich/7Vuw2b"],
            "members": ["admin"]
        }
    ],
    "messages": [
        {"sender": "admin", "text": "Welcome to the Anti Chat Control platform.", "seen": True},
        {"sender": "pedro", "text": "This application runs fully secured.", "seen": False}
    ]
}

ACTIVE_USER = None

def main(page: ft.Page):
    global ACTIVE_USER
    
    page.title = "Anti Chat Control"
    page.theme_mode = ft.ThemeMode.DARK
    page.dark_theme = ft.Theme(primary_color=ft.Colors.BLUE_400)
    page.padding = 15
    page.scroll = "auto"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def navigate_to(view):
        page.clean()
        if not ACTIVE_USER:
            show_auth_screen()
        elif view == "chat":
            show_chat_screen()
        elif view == "groups":
            show_groups_screen()
        elif view == "profile":
            show_profile_screen()
        elif view == "settings":
            show_settings_screen()
        page.update()

    def get_nav_bar(active_index):
        return ft.NavigationBar(
            selected_index=active_index,
            on_change=lambda e: process_nav(e.control.selected_index),
            destinations=[
                ft.NavigationBarDestination(icon=ft.icons.CHAT_BUBBLE_OUTLINED, selected_icon=ft.icons.CHAT_BUBBLE, label="Chats"),
                ft.NavigationBarDestination(icon=ft.icons.GROUPS_OUTLINED, selected_icon=ft.icons.GROUPS, label="Groups"),
                ft.NavigationBarDestination(icon=ft.icons.PERSON_OUTLINE, selected_icon=ft.icons.PERSON, label="Profile"),
                ft.NavigationBarDestination(icon=ft.icons.SETTINGS_OUTLINED, selected_icon=ft.icons.SETTINGS, label="Settings"),
            ],
            bgcolor=ft.Colors.GREY_900,
        )

    def process_nav(index):
        views = ["chat", "groups", "profile", "settings"]
        navigate_to(views[index])

    def show_auth_screen():
        email_input = ft.TextField(label="Gmail Address", width=320, border_color=ft.Colors.BLUE_700)
        pass_input = ft.TextField(label="Password", password=True, can_reveal_password=True, width=320, border_color=ft.Colors.BLUE_700)
        user_input = ft.TextField(label="Unique Username", width=320, visible=False, border_color=ft.Colors.BLUE_700)
        
        info_label = ft.Text("", color=ft.Colors.RED_400)
        register_mode = ft.Ref[bool]()
        register_mode.current = False

        def toggle_mode(e):
            register_mode.current = not register_mode.current
            user_input.visible = register_mode.current
            btn_submit.text = "Register" if register_mode.current else "Login"
            toggle_btn.text = "Or login here" if register_mode.current else "Or register here"
            page.update()

        def submit_auth(e):
            global ACTIVE_USER
            email = email_input.value.strip()
            password = pass_input.value.strip()
            username = user_input.value.strip()

            if not email or not password or (register_mode.current and not username):
                info_label.value = "Please fill all required fields."
                page.update()
                return

            if not email.endswith("@gmail.com"):
                info_label.value = "Registration requires a valid @gmail.com address."
                page.update()
                return

            if register_mode.current:
                if email in DB["users"]:
                    info_label.value = "Email address is already registered."
                else:
                    DB["users"][email] = {
                        "email": email,
                        "password": password,
                        "username": username.lower(),
                        "display_name": username,
                        "phone": "Not assigned",
                        "bio": "Using Anti Chat Control.",
                        "avatar": "https://i.postimg.cc/85zX7f00/logo-shield.png",
                        "banner": "#1a237e",
                        "status": "Online",
                        "status_color": ft.Colors.GREEN_400,
                        "dev_mode": False,
                        "read_receipts": False,
                        "friends": []
                    }
                    ACTIVE_USER = email
                    navigate_to("chat")
            else:
                if email in DB["users"] and DB["users"][email]["password"] == password:
                    ACTIVE_USER = email
                    navigate_to("chat")
                else:
                    info_label.value = "Invalid email or password."
                    page.update()

        btn_submit = ft.ElevatedButton(text="Login", on_click=submit_auth, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, width=200)
        toggle_btn = ft.TextButton(text="Or register here", on_click=toggle_mode)

        page.add(
            ft.Column(
                controls=[
                    ft.Icon(name=ft.icons.SHIELD_ROUNDED, color=ft.Colors.BLUE_400, size=80),
                    ft.Text("ANTI CHAT CONTROL", size=28, weight=ft.FontWeight.BOLD, letter_spacing=2),
                    ft.Text("ACC - PRIVATE COMMUNICATION", size=10, color=ft.Colors.BLUE_200),
                    ft.Container(height=20),
                    email_input,
                    pass_input,
                    user_input,
                    info_label,
                    ft.Container(height=10),
                    btn_submit,
                    toggle_btn
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )

    def show_chat_screen():
        user = DB["users"][ACTIVE_USER]

        call_input = ft.TextField(label="Phone Number", hint_text="+34...", width=200, size=12)
        
        def call_action(e):
            num = call_input.value.strip()
            if num:
                try:
                    subprocess.run(["termux-telephony-call", num])
                except:
                    pass

        btn_call = ft.IconButton(icon=ft.icons.PHONE, icon_color=ft.Colors.GREEN_400, on_click=call_action)

        chat_container = ft.Column(scroll="always", height=280)
        
        def load_messages():
            chat_container.controls.clear()
            for msg in DB["messages"]:
                ticks = ""
                color_tick = ft.Colors.GREY_600
                if user.get("dev_mode") and user.get("read_receipts"):
                    color_tick = ft.Colors.BLUE_400 if msg["seen"] else ft.Colors.GREY_600
                    ticks = " vv"
                
                chat_container.controls.append(
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"@{msg['sender']}", weight=ft.FontWeight.BOLD, size=12, color=ft.Colors.BLUE_300),
                            ft.Row([
                                ft.Text(msg['text'], size=14),
                                ft.Text(ticks, size=10, color=color_tick)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                        ]),
                        bgcolor=ft.Colors.GREY_900,
                        padding=10,
                        border_radius=8,
                        margin=5
                    )
                )

        load_messages()

        msg_input = ft.TextField(hint_text="Type your message...", expand=True, border_color=ft.Colors.GREY_700)

        def send_message(e):
            text = msg_input.value.strip()
            if text:
                DB["messages"].append({"sender": user["username"], "text": text, "seen": False})
                msg_input.value = ""
                load_messages()
                page.update()

        page.add(
            ft.Column([
                ft.Row([call_input, btn_call], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(color=ft.Colors.BLUE_900),
                chat_container,
                ft.Row([msg_input, ft.IconButton(icon=ft.icons.SEND, on_click=send_message)])
            ]),
            get_nav_bar(0)
        )

    def show_groups_screen():
        group_list = ft.Column()

        def refresh_groups():
            group_list.controls.clear()
            for g in DB["groups"]:
                group_list.controls.append(
                    ft.ListTile(
                        leading=ft.CircleAvatar(foreground_image_url=g["photo"]),
                        title=ft.Text(g["name"], weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"Invite Link: {g['invitations'][0]}"),
                        trailing=ft.IconButton(
                            icon=ft.icons.SHARE, 
                            on_click=lambda e, grp=g: copy_link(grp)
                        )
                    )
                )

        def copy_link(g):
            rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
            new_link = f"antich/{rand_str}"
            g["invitations"].append(new_link)
            page.snack_bar = ft.SnackBar(ft.Text(f"Invite link generated: {new_link}"))
            page.snack_bar.open = True
            refresh_groups()
            page.update()

        refresh_groups()

        g_name = ft.TextField(label="Group Name", width=250)
        
        def create_new_group(e):
            name = g_name.value.strip()
            if name:
                rand_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
                DB["groups"].append({
                    "name": name,
                    "photo": "https://i.postimg.cc/85zX7f00/logo-shield.png",
                    "invitations": [f"antich/{rand_str}"],
                    "members": [DB["users"][ACTIVE_USER]["username"]]
                })
                g_name.value = ""
                refresh_groups()
                page.update()

        page.add(
            ft.Column([
                ft.Text("Groups", size=20, weight=ft.FontWeight.BOLD),
                group_list,
                ft.Divider(),
                ft.Row([g_name, ft.ElevatedButton("Create Group", on_click=create_new_group)])
            ]),
            get_nav_bar(1)
        )

    def show_profile_screen():
        user = DB["users"][ACTIVE_USER]

        name_input = ft.TextField(label="Display Name", value=user["display_name"], width=250)
        bio_input = ft.TextField(label="Description", value=user["bio"], width=250)
        avatar_input = ft.TextField(label="Avatar URL", value=user["avatar"], width=250)
        banner_input = ft.TextField(label="Banner Hex Color", value=user["banner"], width=250)
        phone_input = ft.TextField(label="Phone Number", value=user["phone"], width=250)

        def change_status(e):
            statuses = {
                "Online": ft.Colors.GREEN_400,
                "Idle": ft.Colors.ORANGE_400,
                "Do Not Disturb": ft.Colors.RED_400,
                "Invisible": ft.Colors.GREY_400
            }
            user["status"] = e.control.value
            user["status_color"] = statuses[e.control.value]
            page.update()

        status_dropdown = ft.Dropdown(
            label="User Status",
            value=user["status"],
            options=[
                ft.dropdown.Option("Online"),
                ft.dropdown.Option("Idle"),
                ft.dropdown.Option("Do Not Disturb"),
                ft.dropdown.Option("Invisible"),
            ],
            width=250,
            on_change=change_status
        )

        def save_profile(e):
            user["display_name"] = name_input.value
            user["bio"] = bio_input.value
            user["avatar"] = avatar_input.value if avatar_input.value else "https://i.postimg.cc/85zX7f00/logo-shield.png"
            user["banner"] = banner_input.value
            user["phone"] = phone_input.value
            page.snack_bar = ft.SnackBar(ft.Text("Profile updated successfully."))
            page.snack_bar.open = True
            navigate_to("profile")

        profile_card = ft.Container(
            content=ft.Column([
                ft.Container(height=80, bgcolor=user["banner"], border_radius=ft.border_radius.only(top_left=12, top_right=12)),
                ft.Stack([
                    ft.CircleAvatar(foreground_image_url=user["avatar"], radius=40),
                    ft.Container(
                        content=ft.Container(width=15, height=15, bgcolor=user["status_color"], border_radius=10),
                        left=55, top=55
                    )
                ]),
                ft.Text(f"{user['display_name']} (@{user['username']})", size=18, weight=ft.FontWeight.BOLD),
                ft.Text(user["bio"], italic=True, color=ft.Colors.GREY_400),
                ft.Text(f" {user['phone']}", size=12, color=ft.Colors.BLUE_200),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.GREY_900,
            border_radius=12,
            padding=15,
            width=300
        )

        page.add(
            ft.Column([
                profile_card,
                ft.Divider(),
                ft.Text("Edit Profile", weight=ft.FontWeight.BOLD, size=16),
                name_input,
                bio_input,
                avatar_input,
                banner_input,
                phone_input,
                status_dropdown,
                ft.ElevatedButton("Save Changes", on_click=save_profile, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            get_nav_bar(2)
        )

    def show_settings_screen():
        user = DB["users"][ACTIVE_USER]

        def toggle_dev_mode(e):
            user["dev_mode"] = e.control.value
            dev_panel.visible = user["dev_mode"]
            page.update()

        dev_switch = ft.Switch(
            label="Developer Mode",
            value=user.get("dev_mode", False),
            on_change=toggle_dev_mode
        )

        def toggle_read_receipts(e):
            user["read_receipts"] = e.control.value
            page.update()

        dev_panel = ft.Container(
            content=ft.Column([
                ft.Text("Developer Settings", weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400),
                ft.Switch(
                    label="Read Receipts (Double Blue Check)",
                    value=user.get("read_receipts", False),
                    on_change=toggle_read_receipts
                )
            ]),
            visible=user.get("dev_mode", False),
            bgcolor=ft.Colors.BLACK_12,
            padding=15,
            border_radius=8,
            border=ft.border.all(1, ft.Colors.BLUE_900)
        )

        friend_input = ft.TextField(label="Add Friend (Username)", width=250)
        
        def add_friend_action(e):
            name = friend_input.value.strip().lower()
            if name:
                exists = False
                for u in DB["users"].values():
                    if u["username"] == name:
                        exists = True
                        break
                if exists:
                    user["friends"].append(name)
                    page.snack_bar = ft.SnackBar(ft.Text(f"Added @{name} to friends"))
                else:
                    page.snack_bar = ft.SnackBar(ft.Text("User not found."))
                page.snack_bar.open = True
                friend_input.value = ""
                page.update()

        def logout_action(e):
            global ACTIVE_USER
            ACTIVE_USER = None
            navigate_to("auth")

        page.add(
            ft.Column([
                ft.Text("Settings", size=22, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Container(height=10),
                ft.Row([friend_input, ft.IconButton(icon=ft.icons.PERSON_ADD, on_click=add_friend_action)]),
                ft.Divider(),
                dev_switch,
                dev_panel,
                ft.Divider(),
                ft.ElevatedButton("Logout", on_click=logout_action, bgcolor=ft.Colors.RED_800, color=ft.Colors.WHITE, width=200)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            get_nav_bar(3)
        )

    navigate_to("auth")

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
