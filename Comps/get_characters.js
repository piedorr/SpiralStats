'use strict';

var genshindb = require('genshin-db');
var characters = {};

let names = genshindb.characters("names", {matchCategories: true});
names.forEach((name) => {
	let c = genshindb.characters(name);
	characters[c.name] = {
		weapon: c.weapontype,
		element: c.element,
		version: c.version,
		phase: "1.5",
		rarity: parseInt(c.rarity)
	};
});

console.log(JSON.stringify(characters, null, 4));
