#!/usr/bin/node

const request = require('request');
const API_URL = 'https://swapi-api.hbtn.io/api/films/';

if (process.argv.length > 2) {
  const movieId = process.argv[2];
  const url = `${API_URL}${movieId}/`;

  request(url, (err, res, body) => {
    if (err) {
      console.error(err);
      return;
    }

    const characters = JSON.parse(body).characters;

    const fetchCharacterName = (url) => new Promise((resolve, reject) => {
      request(url, (err, res, body) => {
        if (err) {
          reject(err);
          return;
        }
        resolve(JSON.parse(body).name);
      });
    });

    const characterPromises = characters.map(fetchCharacterName);

    Promise.all(characterPromises)
      .then((names) => {
        names.forEach((name) => console.log(name));
      })
      .catch((err) => console.error(err));
  });
}
