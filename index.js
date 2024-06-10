const express = require("express");
const session = require("express-session");
const { google } = require("googleapis");
// const fetch = require("node-fetch");

const app = express();

app.use(
  session({
    secret: "secretKey",
    resave: false,
    saveUninitialized: true,
  })
);

const credentials = require("./creds.json");
const { client_secret, client_id, redirect_uris } = credentials.web;

const oAuth2Client = new google.auth.OAuth2(
  client_id,
  client_secret,
  redirect_uris[0]
);

const API_KEY = "AIzaSyA8EvmpNJttuxsJi6A8lgfooLIuL2divRI"; // Replace with your API key
const SCOPES = [
  "https://www.googleapis.com/auth/fitness.activity.read",
  "https://www.googleapis.com/auth/fitness.heart_rate.read",
  "https://www.googleapis.com/auth/fitness.body.read",
  "https://www.googleapis.com/auth/fitness.sleep.read",
  "https://www.googleapis.com/auth/fitness.reproductive_health.read",
  "https://www.googleapis.com/auth/userinfo.profile",
];

const dataValues = [
  { title: "Calories", type: "com.google.calories.expended" },
  { title: "Heart", type: "com.google.heart_minutes" },
  { title: "Move", type: "com.google.active_minutes" },
  { title: "Steps", type: "com.google.step_count.delta" },
  { title: "Sleep", type: "com.google.sleep.segment" },
];

const getAggregatedDataBody = (dataType, endTime) => {
  return {
    aggregateBy: [{ dataTypeName: dataType }],
    bucketByTime: { durationMillis: 86400000 },
    endTimeMillis: endTime,
    startTimeMillis: endTime - 7 * 86400000,
  };
};

const baseObj = { Calories: 0, Heart: 0, Move: 0, Steps: 0 };

const getWeeklyData = async (endTime, accessToken) => {
  let state = [];
  let promises = [];

  for (let i = 30; i >= 0; i--) {
    let currTime = new Date(endTime - i * 86400000);
    state.push({ ...baseObj, Date: currTime });
  }

  for (const element of dataValues) {
    let body = getAggregatedDataBody(element.type, endTime);

    promises.push(
      fetch(
        `https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate?key=${API_KEY}`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${accessToken}`,
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        }
      )
        .then((response) => response.json())
        .then((data) => {
          for (let idx = 0; idx < 7; idx++) {
            if (data.bucket[idx] && data.bucket[idx].dataset[0]) {
              data.bucket[idx].dataset[0].point.forEach((point) => {
                point.value.forEach((val) => {
                  let extract = val["intVal"] || Math.ceil(val["fpVal"]) || 0;
                  state[idx][element.title] += extract;
                });
              });
            }
          }
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        })
    );
  }

  await Promise.all(promises);
  return state;
};

app.get("/auth/google", (req, res) => {
  const authUrl = oAuth2Client.generateAuthUrl({
    access_type: "offline",
    scope: SCOPES,
  });
  res.redirect(authUrl);
});

app.get("/auth/google/callback", async (req, res) => {
  const { code } = req.query;

  try {
    const { tokens } = await oAuth2Client.getToken(code);
    oAuth2Client.setCredentials(tokens);
    req.session.tokens = tokens;
    res.cookie("access_token", tokens.access_token, { httpOnly: true });
    res.redirect("/");
  } catch (error) {
    console.error("Error retrieving access token:", error);
    res.redirect("/error");
  }
});

app.get("/", async (req, res) => {
  const endTime = Date.now();
  const tokens = req.session.tokens;

  if (!tokens) {
    res.redirect("/auth/google");
    return;
  }

  try {
    const data = await getWeeklyData(endTime, tokens.access_token);
    res.json(data);
  } catch (error) {
    console.error("Error fetching fitness data:", error);
    res.redirect("/error");
  }
});

app.listen(8000, () => {
  console.log("Server is running on port 8000");
});
