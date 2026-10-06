const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
    res.send("Job Portal Backend is Running");
});

app.get("/jobs", (req, res) => {
    res.json([
        {
            title: "AWS DevOps Engineer",
            company: "ABC Technologies",
            location: "Chennai",
            salary: "₹4 LPA - ₹6 LPA"
        },
        {
            title: "Python Developer",
            company: "XYZ Solutions",
            location: "Bangalore",
            salary: "₹3 LPA - ₹5 LPA"
        }
    ]);
});

app.listen(5000, () => {
    console.log("Job Portal Backend running on port 5000");
});
