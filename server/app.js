const express = require("express")
const connectDB = require("./config/db")
const dotenv = require("dotenv")
const dns = require("dns")
const courseRoute = require("./routes/courseRoutes")
const authRoute = require("./routes/authRoutes")
const cors = require("cors")
const app = express()

app.use(cors())

dns.setServers(["1.1.1.1","8.8.8.8"])
dotenv.config()
app.use(express.json())

app.use("/api/auth", authRoute)
 app.use("/api/courses",courseRoute)

// app.get("/welcome",(req,res)=>{
//     res.send("welcome back")

// })

connectDB()

app.listen(3000,()=>{
    console.log("Listening to port")

})