    var WIDTH = document.body.offsetWidth;
    var HEIGHT = document.body.offsetHeight;
    var DIV = {
        width: 50,
        height: 50
    };
    var SPEED = 1000;
    var ANIMATION_DEFAULT = "Quart.easeOut";

    if (HEIGHT > WIDTH){
        alert("For better experience - turn device!");

    }

    var game = new Phaser.Game(WIDTH, HEIGHT, Phaser.AUTO, 'Pluto', {preload: preload, create: create, update: update});
    var command;
    var program;
    var scene;
    var creation;

    var commands = {};
    var programs = [];
    var tiles = [];
    var hero = {};
    var creations = {};

    var program_scroll;
    var background;

    var defaultFont = {font: "25px Arial", fill: "black", align: "center"};

    var command_names = ['forward', 'backward', 'left', 'right', 'lo', 'op'];

    var attempts = 0;

    /**
     * Preload images
     */
    function preload() {

        game.load.image("forward", forward_command_path);
        game.load.image("backward", backward_command_path);
        game.load.image("left", left_command_path);
        game.load.image("right", right_command_path);
        game.load.image("lo", lo_command_path);
        game.load.image("op", op_command_path);

        game.load.image("hero", hero_path + hero_data.type + ".png");

        game.load.image("tile_default", tile_default_path);
        game.load.image("tile_finish", tile_finish_path);


        game.stage.backgroundColor = '#000000';
    }

    /**
     * Creates game
     */
    function create() {
        /**
         * Creates program panel
         */
        function createProgramPanel(){
            //Program
            program = game.add.group();
            program.fixedToCamera = true;
            program.inputEnableChildren = true;
            program.x = 0;
            program.y = 0;
            program.w = WIDTH;
            program.h = DIV.height * 1.5;
            program.cameraOffset = program.position.clone();
            var program_holder = game.add.graphics(0, 0);
            program_holder.beginFill(0xc1c1c1, 0.75);
            program_holder.drawRect(0, 0, program.w, program.h);
            program_holder.endFill();
            program.addChild(program_holder);

            var tmp_scroll = game.add.graphics(0, 0);
            tmp_scroll.beginFill(0xc1c1c1, 1);
            tmp_scroll.drawRect(0, 0, program.w, DIV.height/4);
            tmp_scroll.endFill();
            program_scroll = game.add.sprite(0, program.h - DIV.height/4);
            program_scroll.fixedToCamera = true;
            program_scroll.inputEnabled = true;
            program_scroll.input.enableDrag();
            program_scroll.input.allowVerticalDrag = false;
            program_scroll.input.priorityID = 1;
            program_scroll.cameraOffset = program_scroll.position.clone();
            program_scroll.events.onDragStart.add(programPanelScrollOnDragStart, this);
            program_scroll.events.onDragStop.add(programPanelScrollOnDragStop, this);
            program_scroll.addChild(tmp_scroll);
        }

        /**
         * Creates Panel With Commands
         */
        function createCommandPanel(){
             //Commands
            command = game.add.group();
            command.fixedToCamera = true;
            command.inputEnableChildren = true;
            command.x = (WIDTH - 9.5 * DIV.width)/2;
            command.y = HEIGHT - DIV.height * 1.5;
            command.w = 9.5 * DIV.width;
            command.h = DIV.height * 1.5;
            command.cameraOffset = command.position.clone();
            var command_holder = game.add.graphics(0, 0);
            command_holder.beginFill(0xc1c1c1, 0.75);
            command_holder.drawRect(0, 0, command.w, command.h);
            command_holder.endFill();
            command.addChild(command_holder);


            var x;
            x = DIV.width;
            for (var i in command_names){
                commands[command_names[i]] = command.create(x, 3*DIV.height/4, command_names[i]);
                x += 3 * DIV.width/2;
            }
            for (var key in commands_data){
                commands[key].count = {'value': commands_data[key] };
            }

            for (var key in commands){
                var object = commands[key];
                object.anchor.setTo(0.5, 0.5);
                //Draggable
                object.inputEnabled = true;
                object.input.enableDrag();
                object.events.onDragStart.add(commandPanelCommandOnDragStart, this);
                object.events.onDragStop.add(commandPanelCommandOnDragStop, this);
                // Counters
                var text = object.count.value;
                object.count.text = game.add.text(object.x, object.y  + DIV.height/2 + 5, text, defaultFont, command);
                object.count.text.anchor.setTo(0.5, 0.5);

            }
            // End Commands
        }

        /**
         * Creates game scene
         */
        function createScenePanel(){
            scene = game.add.group();
            scene.x = 0;
            scene.y = DIV.height * 1.5;
            scene.w = WIDTH;
            scene.h = HEIGHT - DIV.height * 1.5 - DIV.height * 1.5;
            scene.direction = 0;

            background = game.add.sprite();
            background.fixedToCamera = true;
            background.cameraOffset.x = scene.x;
            background.cameraOffset.y = scene.y;
            background.inputEnabled = true;
            background.width = scene.w;
            background.height = scene.h;
            background.input.enableDrag();
            background.events.onDragStart.add(sceneBackgroundOnDragStart, this);
            background.events.onDragStop.add(sceneBackgroundOnDragStop, this);
            background.input.priorityID = 0;
            background.originalPosition = background.cameraOffset.clone();

            if (creative_mode){
                var grid = game.add.graphics(0, 0);
                grid.lineStyle(1, 0x33FF00, 1);
                for (var i = 0; i < 2*WIDTH; i+=50){
                    grid.moveTo(i, 0);
                    grid.lineTo(i, 2*WIDTH);
                    grid.moveTo(0, i);
                    grid.lineTo(2*WIDTH, i);
                }
                scene.addChild(grid);
            }


            var x, y, current;
            for (var i in tiles_data){
                x = tiles_data[i].x * DIV.width;
                y = tiles_data[i].y * DIV.height;
                current = scene.create(x, y, tiles_data[i].type);
                tiles.push(current);
            }

            var hero_group = game.add.group()
            hero_group.x = 0;
            hero_group.y = DIV.height * 1.5;
            hero = hero_group.create(hero_data.x * DIV.width + DIV.width/2, hero_data.y * DIV.height + DIV.height/2, "hero");
            hero.anchor.setTo(0.5, 0.5);
            hero.direction  = hero_data.direction;
            hero.angle = hero.direction * 90;
            hero.inputEnabled = true;
            hero.events.onInputDown.add(sceneHeroOnInputDown, this);
            hero.originalPosition = hero.position.clone();
            hero.originalDirection = hero.direction;
            hero.input.priorityID = 2;
        }

        function createCreationPanel() {
            creation = game.add.group();
            creation.fixedToCamera = true;
            creation.inputEnableChildren = true;
            creation.x = (WIDTH - 1.5 * DIV.width);
            creation.y = HEIGHT / 2 - DIV.height * 1.375;
            creation.w = 1.5 * DIV.width;
            creation.h = 2.75 * DIV.height;
            creation.cameraOffset = creation.position.clone();
            var creation_holder = game.add.graphics(0, 0);
            creation_holder.beginFill(0xc1c1c1, 0.75);
            creation_holder.drawRect(0, 0, creation.w, creation.h);
            creation_holder.endFill();
            creation.addChild(creation_holder);

            creations['tile_default'] = creation.create(0.75*DIV.width, 0.75 * DIV.height, 'tile_default')
            creations['tile_finish'] = creation.create(0.75*DIV.width, 2 * DIV.height , 'tile_finish')

            for (var key in creations){
                var object = creations[key];
                object.anchor.setTo(0.5, 0.5);
                //Draggable
                object.inputEnabled = true;
                object.input.enableDrag();
                object.events.onDragStart.add(creationPanelTileOnDragStart, this);
                object.events.onDragStop.add(creationPanelTileOnDragStop, this);
                object.count = {};
                // Counters
                var text = "~";
                object.count.text = game.add.text(object.x + 25, object.y, text, defaultFont, creation);
                object.count.text.anchor.setTo(0.5, 0.5);

            }

            for (var i = 0; i < tiles.length; ++i){
                tiles[i].inputEnabled = true;
                tiles[i].input.enableDrag();
                tiles[i].events.onDragStart.add(sceneTileOnDragStart, this);
                tiles[i].events.onDragStop.add(sceneTileOnDragStop, this);
            	tiles[i].input.priorityID = 1;
            }

            hero.events.onInputDown.removeAll();
            hero.input.enableDrag();
            hero.events.onDragStart.add(sceneHeroOnDragStart, this);
            hero.events.onDragStop.add(sceneHeroOnDragStop, this);
            hero.dragging = false;

            //TODO Add hero turn button
        }

        game.world.setBounds(0, 0, 1920, 1920);
        game.camera.setBoundsToWorld();
        //game.world.resize(MAX_WIDTH, MAX_HEIGHT);


        createScenePanel();
        createProgramPanel();
        createCommandPanel();

        if (creative_mode) {
            createCreationPanel();
        }

        commandPanelCommandsTurn();

        loaded();
    }

    /**
     * Delta commands counter and change it view
     * @param key string command ('forward', 'backward', 'left', 'right', 'lo', 'op')
     * @param delta int change
     */
    function commandPanelDeltaCommandCount(key, delta){
        commands[key].count.value += delta;
        commands[key].count.text.setText(commands[key].count.value);
        if (delta > 0){
            if (key !== 'forward' && key !== 'backward') {
                commandPanelCommandsTurn();
                programPanelCommandsTurn();
            }
        }
    }

    var command_tweens = {};
    //TODO Find any fixes of fast clicking
    /**
     * Turns commands in command panel based on user program
     */
    function commandPanelCommandsTurn() {
        var direction = getHeroDynamicDirection(programPanelCompile(), hero.direction);

        if (direction !== scene.direction) {
            var dir = (direction > scene.direction) ? ("+") : ("-");
            var angle = dir + (Math.abs(direction - scene.direction) * 90).toString();

            for (var i = 0; i < command_names.length - 2; ++i){
                var tmp =  game.add.tween(commands[command_names[i]]).to(
                    {angle: angle}, SPEED, ANIMATION_DEFAULT);

                if (command_tweens[command_names[i]] && command_tweens[command_names[i]].isRunning){
                    command_tweens[command_names[i]].chain(tmp);
                }else{
                    tmp.start();
                }
                command_tweens[command_names[i]] = tmp;
            }

            scene.direction = direction;
        }
    }

    /**
     * Tuns commands in program panel based on user program
     * @param start program panel command sprite index to start turn changes
     */
    function programPanelCommandsTurn(start) {
        start = (typeof start === 'undefined') ? 0 : start;

        for (var i = start; i < programs.length; ++i){
            if (programs[i].key !== 'lo' && programs[i].key !== 'op'){
                var current = programs[i];
                var direction = getHeroDynamicDirection(programPanelCompile(i), hero.direction);
                var current_dir = current.angle / 90;
                while (current_dir < 0){
                    current_dir += 4;
                }
                current_dir %= 4;
                var dir = (direction > current_dir)?("+"):("-");
                var angle = dir + (Math.abs(direction - current_dir)*90).toString();

                game.add.tween(programs[i]).to({angle: angle}, SPEED, ANIMATION_DEFAULT).start();

            }
        }
    }

    /**
     * Adds command sprite to program
     * @param command sprite of selected command
     * @param pointer place where command sprite was dragged or clicked
     */
    function programPanelAddCommand(command, pointer){
        var index = programs.length;
        pointer.x += DIV.width/2;
        //If command was dragged
        if (pointer.y < program.y + program.h){
            for (var i = 0; i < programs.length; ++i){
                if (Phaser.Rectangle.intersects(programs[i].getBounds(), command.getBounds())){
                    if (programs[i].getBounds().centerX < command.getBounds().centerX){
                        index = i + 1; //(i == programs.length)?(i):(i+1)
                    }else {
                        index = i;
                    }
                }
            }
        }

        //Copy command sprite
        var current = program.create(DIV.width/2, 3*DIV.height/4, command.key);
        current.anchor.setTo(0.5, 0.5);
        current.angle = command.angle;
        current.inputEnabled = true;
        current.input.enableDrag();
        current.events.onDragStart.add(programPanelCommandOnDragStart, this);
        current.events.onDragStop.add(programPanelCommandOnDragStop, this);
        current.input.allowVerticalDrag = false;
        // Add to program
        programs.splice(index, 0, current);
        //Align commands in program view
        programPanelAlignCommands();
        //Commands turning
        if (index < programs.length - 1){
            programPanelCommandsTurn(index);
            commandPanelCommandsTurn();
        }else{
            if (command.key !== 'forward' && command.key !== 'backward') {
                commandPanelCommandsTurn();
                programPanelCommandsTurn();
            }
            //TODO Move scroll to the end.
        }

        programPanelScrollResize();
    }

    /**
     * Align commands in program view.
     * To make them follow each other after deleting or adding some in custom place.
     */
    function programPanelAlignCommands(){
        // TODO Maybe animation
        if (programs.length == 0){
            return;
        }
        if (programs[0].x > 0){
            programs[0].x = DIV.width/2;
        }
        for (var i = 1; i < programs.length; ++i){
            programs[i].alignTo(programs[i-1], Phaser.RIGHT_CENTER);
        }
    }

    /**
    * Resizes panel scroller based on program panel content
    */
    function programPanelScrollResize() {
        var last = programs[programs.length - 1];
        if (last){
            var max_width = last.x + last.width - programs[0].x;
            var scroll_width = WIDTH*WIDTH / max_width;

            var tmp_scroll = game.add.graphics(0, 0);
            tmp_scroll.beginFill(0xc1c1c1, 1);
            tmp_scroll.drawRect(0, 0, scroll_width, DIV.height/4);
            tmp_scroll.endFill();
            program_scroll.removeChildren(0, 1);
            program_scroll.addChild(tmp_scroll);


        }
    }

    /**
    * Moves program panle in case of moving of scroller in some scale
    * @param sprite of scroller
    * @param position fake position of scroller (optional)
    */
    function programPanelScrollMove(sprite, position){
        if (position){
            sprite.cameraOffset.x = position;
        }
        //TODO Max position scroll dont show last command Maybe it's calculation problem
        if (sprite.cameraOffset.x < 0){
            sprite.cameraOffset.x = 0;
        }else if (sprite.cameraOffset.x + sprite.getChildAt(0).width > WIDTH){
            sprite.cameraOffset.x = WIDTH - sprite.getChildAt(0).width;
        }


        var last = programs[programs.length - 1];
        if (last) {
            var max_width = last.x + last.width - programs[0].x;
            var deltaX = (sprite.originalPosition.x - sprite.cameraOffset.x) * max_width/WIDTH;
            programs[0].x += deltaX;
            programPanelAlignCommands();
        }
    }
    /**
     * Gets direction after running pure program of commands
     * @param pure program of simple commands
     * @param starting_dir direction from the start
     * @returns {number} direction (0 - up, 1 - right, 2 - down, 3 - left)
     */
    function getHeroDynamicDirection(pure, starting_dir){
        var direction = (typeof starting_dir === 'undefined') ? 0 : starting_dir;

        for (var i = 0; i < pure.length; ++i){
            if (pure[i] === 'left'){
                --direction;
            }
            if (pure[i] === 'right'){
                ++direction;
            }
        }

        while(direction < 0){
            direction += 4;
        }
        direction %= 4;

        return direction;
    }

    var tween;

    /**
     * Updates game frames
     */
    function update() {
        if (sceneCheckHeroAndTilesIntersection().length < 1 && !hero.dragging){
            game.camera.shake(0.01,  500);
            gameSuccess(false);
        }
        //game.debug.cameraInfo(this.game.camera, 0, 200);
        //game.debug.spriteInfo(hero, 32, 32);
        //game.debug.spriteBounds(hero);
    }

    /**
     * Checking successes of program created by user
     */
    function gameCheckSucceed() {
            var tiles = sceneCheckHeroAndTilesIntersection();
            var success = false;
            for (var i in tiles){
                if (tiles[i].key === "tile_finish"){
                    success = true;
                }
            }
            gameSuccess(success);
        }

    /**
     * Start of program running
     * Creates tweens and runs first
     */
    function gameStart(){
        if (programs.length > 0) {
            hero.input.enabled = false;
            ++attempts;
            tween = createExecution(programPanelCompile());
            if (tween.length > 0) {
                tween[0].start();
                tween[tween.length - 1].onComplete.add(gameCheckSucceed, this);
            }
        }
    }

    /**
     * Reaction to end of program executing
     * @param success bool
     */
    function gameSuccess(success) {
        if (success){
            if (creative_mode) {
                hero.position = hero.originalPosition.clone();
                var level = {'hero':
                                    {'x': Math.floor(hero.x/DIV.width),
                                     'y': Math.floor(hero.y/DIV.height),
                                     'direction':   hero.direction
                                    },
                            'tilemap': [],
                            'commands': {
                                    'forward': 0,
                                    'backward': 0,
                                    'left': 0,
                                    'right': 0,
                                    'lo': 0,
                                    'op': 0
                                    }
                };
                for (var i = 0; i < tiles.length; ++i){
                    level.tilemap.push({"type": tiles[i].key, "x": Math.floor(tiles[i].x/DIV.width), "y": Math.floor(tiles[i].y/DIV.height)});
                }
                level.tilemap = JSON.stringify(level.tilemap);
                for (var i = 0; i < programs.length; ++i){
                    level.commands[programs[i].key] += 1;
                }
                document.getElementsByName('level')[0].value = JSON.stringify(level);
                document.getElementsByName('name')[0].value = prompt("Set level name:", level_name);
                document.forms['creator'].submit();
            }else{
                var pure = [];
                for (var i = 0; i < programs.length; ++i) {
                    pure.push(programs[i].key);
                }
                document.getElementsByName("attempts")[0].value = attempts;
                document.getElementsByName("program")[0].value = JSON.stringify(pure);
                document.forms['record'].submit();
            }
        }else{
            game.tweens.removeAll();
            sceneHeroReset();
        }
    }

    /**
     * Compiles user program to simple commands (transfer loops into simple commands)
     * @param to int specific sprite index to which compilation is going
     * @returns {Array} strings of simple commands
     */
    function programPanelCompile(to){
        to = (typeof to === 'undefined') ? programs.length : to;

        var pure = [];
        for (var i = 0; i < to; ++i){
            var current =  programs[i].key;
            pure.push(current);
        }

        // LOOP handle
        var pair = 0;
        for (i = 0; i < pure.length; ++i){
            if (pure[i] === "lo"){
                --pair;
            }else if (pure[i] === "op"){
                if (pair === 0){
                    pure.splice(0, 0, "lo");
                    ++i;
                }else{
                    ++pair;
                }
            }
        }

        while(pair < 0){
            pure.push("op");
            ++pair;
        }

        for (i = 0; i < pure.length; ++i){
            if (pure[i] === "lo"){
                pair -= 1;
                var j = i + 1;
                do{
                    if (pure[j] === "lo"){
                        pair -= 1;
                    }
                    if (pure[j] === "op"){
                        pair += 1;
                    }
                    ++j;
                }while (pair !== 0 && j < pure.length);

                if (pair === 0){
                    var double = pure.slice(i+1, j-1);
                    pure.splice(j-1, 1);
                    pure.splice.apply(pure, [i, 1].concat(double));
                }else{
                    return [];
                }
                --i;
            }
        }
        return pure;
    }

    /**
     * Creates linked tween which based on user program. It makes hero move like user said.
     * @param program pure program
     * @returns {Array} tween of program
     */
    function createExecution(program){
        var result = [];
        var len = DIV.height;
        var direction = hero.direction;
        var x = hero.x;
        var y = hero.y;

        for (var i in program){
            var tmp;
            var dx = 0, dy = 0;
            switch (direction){
                case 0:
                    dy = -len;
                    break;
                case 1:
                    dx = len;
                    break;
                case 2:
                    dy = len;
                    break;
                case 3:
                    dx = -len;
                    break;
            }

            if (program[i] === 'forward') {
                x += dx;
                y += dy;
                tmp = game.add.tween(hero).to({x: x, y: y}, SPEED, ANIMATION_DEFAULT);
            }else if(program[i] === 'backward'){
                x -= dx;
                y -= dy;
                tmp = game.add.tween(hero).to({x: x, y: y}, SPEED, ANIMATION_DEFAULT);
            }else if(program[i] === 'left'){
                tmp = game.add.tween(hero).to({angle: '-90'}, SPEED, ANIMATION_DEFAULT);
                direction = (direction + 3) % 4;
            }else if(program[i] === 'right'){
                tmp = game.add.tween(hero).to({angle: '+90'}, SPEED, ANIMATION_DEFAULT);
                direction = (direction + 5) % 4;;
            }

            result.push(tmp);
            if (result.length > 1){
                result[result.length - 2].chain(tmp);
            }
        }
        return result;
    }

    /**
     * Checking if hero is on tiles at this moment
     * @returns {Array} of intersected tiles
     */
    function sceneCheckHeroAndTilesIntersection(){
        var result = [];
        for (var i in tiles){
            var point = new Phaser.Point(hero.getBounds().centerX, hero.getBounds().centerY);
            if (Phaser.Rectangle.containsPoint(tiles[i].getBounds(), point)){
                result.push(tiles[i]);
            }
        }
        return result;
    }


    function sceneClearTilePlace(sprite, position){
        var x = Math.floor((sprite.x + creation.cameraOffset.x - scene.x + game.camera.x)/DIV.width)*DIV.width;
    	var y = Math.floor((sprite.y + creation.cameraOffset.y - scene.y + game.camera.y)/DIV.height)*DIV.height;
        for (var i = 0; i < tiles.length; ++i){
    		if (tiles[i].x === x && tiles[i].y === y){
    			if (tiles[i].key === sprite.key){
    				return;
    			}else{
    				tiles[i].destroy();
    			}
    			tiles.splice(i, 1)
    		}
    	}
    }
    /**
     * Add tiles on scene in creative mode
     * @param sprite tile sprite
     * @param position pointer position
     */
    function sceneAddTile(sprite, position){
    	var x = Math.floor((sprite.x + creation.cameraOffset.x - scene.x + game.camera.x)/DIV.width)*DIV.width;
    	var y = Math.floor((sprite.y + creation.cameraOffset.y - scene.y + game.camera.y)/DIV.height)*DIV.height;

    	sceneClearTilePlace(sprite, position);

    	var tile = scene.create(x, y, sprite.key);
    	tile.inputEnabled = true;
        tile.input.enableDrag();

    	//tile.events.onInputDown.add(sceneTileOnInputDown, this);
    	tile.events.onDragStart.add(sceneTileOnDragStart, this);
    	tile.events.onDragStop.add(sceneTileOnDragStop, this);
        tile.input.priorityID = 1;
    	tiles.push(tile)
    }

    /**
     * Resets hero state.
     */
    function sceneHeroReset() {
        hero.position = hero.originalPosition.clone();
        hero.direction = hero.originalDirection;
        hero.angle = hero.direction * 90;
        hero.input.enabled = true;
    }

    /////////////////////
    ///////Events///////
    ////////////////////
    function commandPanelCommandOnDragStart(sprite, pointer) {
        sprite.originalPosition = sprite.position.clone();
        sprite.position = pointer;
    }

    function commandPanelCommandOnDragStop(sprite, pointer) {
        if (sprite.count.value > 0 || creative_mode){
            // Camera offset correction
            var ptr = pointer;
            ptr.y += command.y;
            programPanelAddCommand(sprite, ptr);
            commandPanelDeltaCommandCount(sprite.key, -1);
        }
        sprite.position = sprite.originalPosition;
    }

    function creationPanelTileOnDragStart(sprite, pointer) {
        sprite.originalPosition = sprite.position.clone()
    }

    function creationPanelTileOnDragStop(sprite, pointer) {
        sceneAddTile(sprite, pointer);
        sprite.position = sprite.originalPosition.clone();
    }

    function programPanelCommandOnDragStart(sprite, pointer) {
        sprite.originalPosition = sprite.position.clone();
    }

    function programPanelCommandOnDragStop(sprite, pointer) {
        var index = programs.indexOf(sprite);
        programs.splice(index, 1);
        if (Math.abs(sprite.x - sprite.originalPosition.x) > sprite.width/2){
            programPanelAddCommand(sprite, pointer);
        }else{
           commandPanelDeltaCommandCount(sprite.key, 1);
        }
        sprite.destroy();
        programPanelAlignCommands();
    }

    function programPanelScrollOnDragStart(sprite, pointer) {
        sprite.originalPosition = sprite.cameraOffset.clone();
    }

    function programPanelScrollOnDragStop(sprite, pointer) {
        programPanelScrollMove(sprite);
    }

    function sceneBackgroundOnDragStart(sprite, pointer){
        sprite.originalPosition = sprite.cameraOffset.clone();
    }

    function sceneBackgroundOnDragStop(sprite, pointer){
        var x = sprite.originalPosition.x - sprite.cameraOffset.x;
        var y = sprite.originalPosition.y - sprite.cameraOffset.y;
        x += game.camera.x;
        y += game.camera.y;

        var animation = game.add.tween(game.camera).to({x: x, y: y}, SPEED, ANIMATION_DEFAULT);
        animation.start();

        sprite.fixedToCamera = true;
        //IDK But it works
        sprite.cameraOffset.x = scene.x;
        sprite.cameraOffset.y = scene.y;
    }


    function sceneHeroOnDragStart(sprite, pointer){
        sprite.originalPosition = sprite.position.clone()
        sprite.dragging = true;
    }

    function sceneHeroOnDragStop(sprite, pointer) {
        var distance = Phaser.Point.distance(sprite.originalPosition, sprite.position);
        sprite.dragging = false;
        if (distance > (DIV.height + DIV.width)/4) {
            var x = Math.floor(sprite.x / DIV.width) * DIV.width;
            var y = Math.floor(sprite.y / DIV.height) * DIV.height;
            sprite.x = x + sprite.width/2;
            sprite.y = y + sprite.height/2;
        }else{
            sprite.position = sprite.originalPosition.clone();
            sceneHeroOnInputDown(sprite, pointer);
        }
    }

    function sceneTileOnDragStart(sprite, pointer){
    	sprite.originalPosition = sprite.position.clone();
    }

    function sceneTileOnDragStop(sprite, pointer){
        if (Phaser.Point.distance(sprite.originalPosition, sprite.position) < (DIV.width + DIV.height)/4){
    	    var index = tiles.indexOf(sprite);
            tiles[index].destroy();
            tiles.splice(index, 1);
        }else{
            var x = Math.floor((sprite.x)/DIV.width)*DIV.width;
    	    var y = Math.floor((sprite.y)/DIV.height)*DIV.height;
            sprite.x = x;
            sprite.y = y;
            sceneClearTilePlace(sprite, pointer);
        }
    }

    function sceneHeroOnInputDown(sprite, pointer) {
        gameStart();
    }