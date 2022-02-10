const mix = require("laravel-mix");
const path = require("path");
const fs = require("fs");

function addStaticLink(appName) {
  return {
    symlink: `static/${appName}_app`,
    dest: `${appName}/static`,
  };
}

function appBuildPath(appName) {
  return `static/${appName}_app/${appName}/build`;
}

const apps = [
  addStaticLink("common"),
  addStaticLink("subscriptions"),
  addStaticLink("my_auth"),
];

// The actual symlink entity in the file system
const source = "static/subscriptions";

// Where the symlink should point to
const absolute_target = "subscriptions/static";

//const target = path.relative(path.dirname(source), absolute_target);

apps.forEach((app) => {
  if (fs.existsSync(app.symlink)) {
    console.log(app.symlink);
    return;
  }
  const target = path.relative(path.dirname(app.symlink), app.dest);
  console.log(target);
  fs.symlinkSync(target, app.symlink);
});

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel applications. By default, we are compiling the CSS
 | file for the application as well as bundling up all the JS files.
 |
 */
mix.setPublicPath(`./`);

mix
  .js("subscriptions/resources/js/index.js", appBuildPath("subscriptions"))
  .js("my_auth/resources/js/index.js", appBuildPath("my_auth"))
  .extract(["axios"], `${appBuildPath("common")}/vendor.js`);

//   .postCss("resources/css/app.css", "public/css", [
//     //
//   ]);

if (mix.inProduction()) {
  mix.version();
}

mix.after(stats => {
  if(!fs.existsSync('./mix-manifest.json')){
    return;
  }

  fs.renameSync('./mix-manifest.json', `${appBuildPath("common")}/mix-manifest.json`);
});