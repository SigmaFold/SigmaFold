import fs from 'fs';

function native_fold(n) {
    // load paths json if it exists
    try {
      var old_paths = JSON.parse(fs.readFileSync('../data/paths.json'));
      // Convert every path to a list of tuples
      if (old_paths[0].length <= n) {
        old_paths = old_paths.map((path) => path.map((point) => [point[0], point[1]]));
      } else {
        old_paths = []; // the info stored is too big - start from scratch
      }
    } catch (err) {
      old_paths = [];
    }
  
    let dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]];
  
    let paths = []; // new paths to be generated
  
    function generate_paths(x, y, visited, path) {
      if (path.length === n) {
        paths.push(path);
        return;
      } else {
        for (let dir of dirs) {
          let new_x = x + dir[0];
          let new_y = y + dir[1];
          if (!visited.has([new_x, new_y])) {
            visited.add([new_x, new_y]);
            generate_paths(new_x, new_y, visited, path.concat([[new_x, new_y]]));
            visited.delete([new_x, new_y]);
          }
        }
      }
    }
  
    // If the input path is empty start from scratch
    if (!old_paths.length) {
      generate_paths(0, 1, new Set([[0, 0], [0, 1]]), [[0, 0], [0, 1]]); // start at (0, 1) to avoid double counting
      old_paths = paths;
    } else {
      for (let idx in old_paths) {
        let path = old_paths[idx];
        let last_point = path[path.length - 1];
        // Reassign that path to the new paths generated
        generate_paths(last_point[0], last_point[1], new Set(path.map((point) => [point[0], point[1]])), path);
        old_paths.splice(idx, 1);
        old_paths = old_paths.concat(paths);
        paths = [];
      }
    }
  
    // Json serialize the path and save the file to the data folder
    fs.writeFileSync('../data/paths.json', JSON.stringify(old_paths));
    console.log(old_paths.length)
    return old_paths;
  }

native_fold(15);
  