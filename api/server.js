const express= require("express")
const app=express()
const mongoose=require("mongoose")
const routesUrls=require("./routes/routes")
const cors=require("cors")

mongoose.connect("mongodb+srv://jagdish2002bhatt:Jagdish2002@dineeats.u7oe5zr.mongodb.net/",()=>console.log("Database connected"))

app.use(express.json())
app.use(cors())
app.use('/app',routesUrls)
app.use('/app/book',routesUrls)


app.listen(4000,()=>console.log("server is up and running"))