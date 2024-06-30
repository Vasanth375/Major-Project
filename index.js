// const express = require("express");
// const session = require("express-session");
// const { google } = require("googleapis");

// const app = express();

// app.use(
//   session({
//     secret: "secretKey",
//     resave: false,
//     saveUninitialized: true,
//   })
// );

// const credentials = require("./creds.json");
// const { client_secret, client_id, redirect_uris } = credentials.web;

// const oAuth2Client = new google.auth.OAuth2(
//   client_id,
//   client_secret,
//   redirect_uris[0]
// );

// const API_KEY = "AIzaSyA8EvmpNJttuxsJi6A8lgfooLIuL2divRI"; // Replace with your API key
// const SCOPES = [
//   "https://www.googleapis.com/auth/fitness.activity.read",
//   "https://www.googleapis.com/auth/fitness.heart_rate.read",
//   "https://www.googleapis.com/auth/fitness.body.read",
//   "https://www.googleapis.com/auth/fitness.sleep.read",
//   "https://www.googleapis.com/auth/fitness.reproductive_health.read",
//   "https://www.googleapis.com/auth/userinfo.profile",
// ];

// const dataValues = [
//   { title: "Calories", type: "com.google.calories.expended" },
//   { title: "Heart", type: "com.google.heart_minutes" },
//   { title: "Move", type: "com.google.active_minutes" },
//   { title: "Steps", type: "com.google.step_count.delta" },
//   { title: "Sleep", type: "com.google.sleep.segment" },
// ];

// const getAggregatedDataBody = (dataType, endTime) => {
//   return {
//     aggregateBy: [{ dataTypeName: dataType }],
//     bucketByTime: { durationMillis: 86400000 },
//     endTimeMillis: endTime,
//     startTimeMillis: endTime - 7 * 86400000,
//   };
// };

// const baseObj = { Calories: 0, Heart: 0, Move: 0, Steps: 0 };

// const getWeeklyData = async (endTime, accessToken) => {
//   let state = [];

//   for (let i = 6; i >= 0; i--) {
//     let currTime = new Date(endTime - i * 86400000);
//     state.push({ ...baseObj, Date: currTime.toISOString().split("T")[0] });
//   }

//   const fetchData = async (element) => {
//     let body = getAggregatedDataBody(element.type, endTime);

//     try {
//       const response = await fetch(
//         `https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate?key=${API_KEY}`,
//         {
//           method: "POST",
//           headers: {
//             Authorization: `Bearer ${accessToken}`,
//             Accept: "application/json",
//             "Content-Type": "application/json",
//           },
//           body: JSON.stringify(body),
//         }
//       );
//       const data = await response.json();

//       data.bucket.forEach((bucket, idx) => {
//         if (bucket.dataset[0].point.length > 0) {
//           bucket.dataset[0].point.forEach((point) => {
//             point.value.forEach((val) => {
//               let extract = val["intVal"] || Math.ceil(val["fpVal"]) || 0;
//               state[idx][element.title] += extract;
//             });
//           });
//         }
//       });
//     } catch (error) {
//       console.error(`Error fetching data for ${element.title}:`, error);
//     }
//   };

//   await Promise.all(dataValues.map(fetchData));

//   return state;
// };

// app.get("/auth/google", (req, res) => {
//   const authUrl = oAuth2Client.generateAuthUrl({
//     access_type: "offline",
//     scope: SCOPES,
//   });
//   res.redirect(authUrl);
// });
// // add this uri to the oauth id
// // http://localhost:8000/auth/google/callback
// app.get("/auth/google/callback", async (req, res) => {
//   const { code } = req.query;

//   try {
//     const { tokens } = await oAuth2Client.getToken(code);
//     oAuth2Client.setCredentials(tokens);
//     req.session.tokens = tokens;
//     res.cookie("access_token", tokens.access_token, { httpOnly: true });
//     res.redirect("/");
//   } catch (error) {
//     console.error("Error retrieving access token:", error);
//     res.redirect("/error");
//   }
// });

// app.get("/", async (req, res) => {
//   const endTime = Date.now();
//   const tokens = req.session.tokens;

//   if (!tokens) {
//     res.redirect("/auth/google");
//     return;
//   }

//   try {
//     const data = await getWeeklyData(endTime, tokens.access_token);
//     res.json(data);
//   } catch (error) {
//     console.error("Error fetching fitness data:", error);
//     res.redirect("/error");
//   }
// });

// app.listen(8000, () => {
//   console.log("Server is running on port 8000");
// });

const express = require("express");
const session = require("express-session");
const { google } = require("googleapis");

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

const SCOPES = [
  "https://www.googleapis.com/auth/fitness.activity.read",
  "https://www.googleapis.com/auth/fitness.heart_rate.read",
  "https://www.googleapis.com/auth/fitness.body.read",
  "https://www.googleapis.com/auth/fitness.sleep.read",
  "https://www.googleapis.com/auth/fitness.reproductive_health.read",
  "https://www.googleapis.com/auth/userinfo.profile",
];


const getRealTimeData = async (accessToken) => {
  const dataTypes = {
    heartRate: "com.google.heart_rate.bpm",
    steps: "com.google.step_count.delta",
    activeMinutes: "com.google.active_minutes",
  };
  
  const currentTimeMillis = Date.now();
  const startTimeMillis = currentTimeMillis - 60 * 60 * 1000; // last hour
  const fetch = (await import("node-fetch")).default; // Dynamically import node-fetch

  const fetchData = async (dataType) => {
    const dataSourceResponse = await fetch(
      `https://www.googleapis.com/fitness/v1/users/me/dataSources?dataTypeName=${dataType}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          Accept: "application/json",
        },
      }
    );

    const dataSources = await dataSourceResponse.json();

    if (!dataSources.dataSource || dataSources.dataSource.length === 0) {
      return null;
    }

    const dataSourceId = dataSources.dataSource[0].dataStreamId;

    const datasetId = `${startTimeMillis}-${currentTimeMillis}`;

    const datasetResponse = await fetch(
      `https://www.googleapis.com/fitness/v1/users/me/dataSources/${dataSourceId}/datasets/${datasetId}`,
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          Accept: "application/json",
        },
      }
    );

    const dataset = await datasetResponse.json();

    let value = 0;
    if (dataset.point && dataset.point.length > 0) {
      dataset.point.forEach((point) => {
        point.value.forEach((val) => {
          value += val.intVal || val.fpVal || 0;
        });
      });
    }

    return value;
  };

  const heartRate = await fetchData(dataTypes.heartRate);
  const steps = await fetchData(dataTypes.steps);
  const activeMinutes = await fetchData(dataTypes.activeMinutes);

  return {
    heartRate,
    steps,
    activeMinutes,
  };
};

const verifyWatchConnection = async (accessToken) => {
  try {
    const response = await fetch(
      "https://www.googleapis.com/fitness/v1/users/me/dataSources",
      {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
          Accept: "application/json",
        },
      }
    );

    const dataSources = await response.json();
    const watchConnected = dataSources.dataSource.some((source) =>
      source.device && source.device.type === "watch"
    );

    return watchConnected;
  } catch (error) {
    console.error("Error verifying watch connection:", error);
    return false;
  }
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
  const tokens = req.session.tokens;

  if (!tokens) {
    res.redirect("/auth/google");
    return;
  }

  try {
    const watchConnected = await verifyWatchConnection(tokens.access_token);
    if (!watchConnected) {
      res.json({ error: "No connected watch found." });
      return;
    }

    const realTimeData = await getRealTimeData(tokens.access_token);
    res.json(realTimeData);
  } catch (error) {
    console.error("Error fetching fitness data:", error);
    res.redirect("/error");
  }
});

app.listen(8000, () => {
  console.log("Server is running on port 8000");
});
