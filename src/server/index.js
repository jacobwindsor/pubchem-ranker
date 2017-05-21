const express = require('express');
const app = express();

app.set('views', './src');
app.set('view engine', 'hbs');

app.get('/', (req, res) => {
  res.send('Hello');
});

app.listen(3000, () => {
  console.log('listening on port 3000');
});
