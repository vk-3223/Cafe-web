import folium
from flask import Flask,render_template
import pandas

user_input = input("do you want add some new cafe Yes or No: ").lower()

if user_input=="yes":
    from sqlite3 import Row
    from backend import Database
    from tkinter import *

    database = Database("cafe.db")
    global selected_tuple


    def get_selected_row(event):
        global selected_tuple

        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0,END)
        e1.insert(END,selected_tuple[1])
        e2.delete(0,END)
        e2.insert(END,selected_tuple[2])
        e3.delete(0,END)
        e3.insert(END,selected_tuple[3])
        e4.delete(0,END)
        e4.insert(END,selected_tuple[4])
    

        

    def viwee_command():
        list1.delete(0,END)
        for i in database.viwe():
            list1.insert(END,i)

    def viwe_serach():
        list1.delete(0,END)
        for i in database.search(cafe_text.get(),link_text.get(),lat_text.get(),lon_text.get()):
            list1.insert(END,i)

    def entry_command():
        database.insert(cafe_text.get(),link_text.get(),lat_text.get(),lon_text.get())
        list1.delete(0,END)
        list1.insert(END,(cafe_text.get(),link_text.get(),lat_text.get(),lon_text.get()))

    def delete_comand():
        database.delete(selected_tuple[0])     

    def update_comand():
        database.update(selected_tuple[0],cafe_text.get(),link_text.get(),lat_text.get(),lon_text.get())  

    window = Tk()

    window.title("cafe data")

    l1 = Label(window,text="Nmae")
    l1.grid(row=0,column=0)


    l2 = Label(window,text="map_url")
    l2.grid(row=0,column=2)

    l3 = Label(window,text="lat")
    l3.grid(row=1,column=0)

    l4 = Label(window,text="lon")
    l4.grid(row=1,column=2)

    cafe_text = StringVar()
    e1 = Entry(window,textvariable=cafe_text)
    e1.grid(row=0,column=1)

    link_text = StringVar()
    e2 = Entry(window,textvariable=link_text)
    e2.grid(row=0,column=3)

    lat_text = StringVar()
    e3 = Entry(window,textvariable=lat_text)
    e3.grid(row=1,column=1)

    lon_text = StringVar()
    e4 = Entry(window,textvariable=lon_text)
    e4.grid(row=1,column=3)

    list1 = Listbox(window,height=6,width=35)
    list1.grid(row=2,column=0,rowspan=6,columnspan=2)

    list1.bind("<<ListboxSelect>>",get_selected_row)

    sb1 = Scrollbar(window)
    sb1.grid(row=2,column=2,rowspan=6)

    list1.configure(yscrollcommand=sb1.set)
    sb1.configure(command=list1.yview)   

    b1 = Button(window,text="View call",width=12,command=viwee_command)
    b1.grid(row=2,column=3)

    b2 = Button(window,text="Search",width=12,command=viwe_serach)
    b2.grid(row=3,column=3)

    b3 = Button(window,text="Add entry",width=12,command=entry_command)
    b3.grid(row=4,column=3)

    b4 = Button(window,text="upedate selected",width=12,command=update_comand)
    b4.grid(row=5,column=3)

    b5 = Button(window,text="Delete",width=12,command=delete_comand)
    b5.grid(row=6,column=3)

    b6 = Button(window,text="close",width=12,command=window.destroy)
    b6.grid(row=7 ,column=3)



    window.mainloop()


else:

    data = pandas.read_csv("final_file.csv")

    m = folium.Map(location=[51.5072,0.1276], tiles="OpenStreetMap", zoom_start=10)
    lat = list(data["lat"])
    lon = list(data["lon"])
    name = list(data["name"])
    map_url = list(data["map_url"])
    img_url = list(data["img_url"])
    coffe_price = list(data["coffee_price"])

    fgv = folium.FeatureGroup(name="cafe")

    for lt,lo,nn,map_u,img_u,coffe in zip(lat,lon,name,map_url,img_url,coffe_price):
        fgv.add_child(folium.Marker(location=[lt,lo],popup=(f"cafe : {nn} \n\n cafe_link : {map_u} \n\n coffe_price : {coffe}"),icon=folium.Icon(color="blue")))
    m.add_child(fgv)

    app = Flask(__name__)
    @app.route('/')
    def html_file():
        return render_template('index.html')

    @app.route('/map')
    def map_file():
        return m._repr_html_() 

    if __name__==("__main__"):
        app.run(debug=1,port=3223)
