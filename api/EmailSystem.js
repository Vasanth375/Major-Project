function sendEmail() {
  Email.send({
    Host: "smtp.gmail.com",
    port: 465,
    Username: "nimmalapremkumar8@gmail.com",
    Password: "vasanth9989",
    To: "nimmalapremkumar8@gmail.com",
    From: "nimmalavasanthsai@gmail.com",
    Subject: "Sending Email using javascript",
    Body: "Well that was easy!!",
  }).then(function (message) {
    alert("mail sent successfully");
  });
}

module.exports = sendEmail;
