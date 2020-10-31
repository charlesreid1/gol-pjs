/*jslint onevar: true, undef: false, nomen: true, eqeqeq: true, plusplus: false, bitwise: true, regexp: true, newcap: true, immed: true  */

/**
 * Game of Life - JS & CSS
 * http://pmav.eu
 * 04/Sep/2010
 *
 * Modifications by charles reid
 * 12 February 2018
 * 11 July 2019
 * 26 October 2020
 */

(function () {

  // The logic to parse what input parameters the user provided
  // lives in loadConfig()


  // Constants

  // Colors
  var realBackgroundColor = "#272b30";
  var gridStrokeColor1    = "#3a3a3a";
  var mapZoneStrokeColor  = "#dddddd";
  var grays = ["#3a3a3a", "#404040"];

  var GOL = {

    defaultGameApiResult: {
      id: '0000-0000-0000',
      team1Name: 'Purple',
      team1Color: '#9963AB',
      team2Name: 'Orange',
      team2Color: '#E86215',
      map: {
        id: 1,
        mapName: 'Main Map',
        mapZone1Name: 'Zone 1',
        mapZone2Name: 'Zone 2',
        mapZone3Name: 'Zone 3',
        mapZone4Name: 'Zone 4',
        initialConditions1: '[{"39":[60]},{"40":[62]},{"41":[59,60,63,64,65]}]',
        initialConditions2: '[{"23":[30]},{"22":[32]},{"21":[29,30,33,34,35]}]',
        columns: 100,
        rows: 100,
        cellSize: 7
      }
    },

    defaultMap : {
      initialConditions1: '[{"39":[60]},{"40":[62]},{"41":[59,60,63,64,65]}]',
      initialConditions2: '[{"23":[30]},{"22":[32]},{"21":[29,30,33,34,35]}]',
      columns: 100,
      rows: 100,
      cellSize: 7
    },

    teamNames: [],
    teamColors: [],

    columns : 0,
    rows : 0,
    cellSize: 0,

    waitTime: 0,
    generation : 0,

    running : false,
    autoplay : false,


    // Clear state
    clear : {
      schedule : false
    },


    // Average execution times
    times : {
      algorithm : 0,
      gui : 0
    },

    // DOM elements
    element : {
      generation : null,
      livecells : null,
      livecells1 : null,
      livecells2 : null,
      victory: null,
      coverage: null,
      territory1: null,
      territory2: null,
      team1color: null,
      team1name: null,
      team2color: null,
      tam2name: null,
      messages : {
        layout : null
      }
    },

    // Initial state
    // Set in loadConfig()
    initialState1 : null,
    initialState2 : null,

    // Trail state
    trail : {
      current: false,
      schedule : false
    },


    // Grid style
    grid : {
      current : 0,
      mapOverlay : false,

      schemes : [
        {
          color : gridStrokeColor1,
        },
        {
          color : '', // Special case: 0px grid
        },
      ],
    },


    // Zoom level
    //
    // columns/rows/cellSize are either set by the map (game mode)
    // or set by the user via the schemes (sandbox mode)
    zoom : {
      current : 0,
      schedule : false,

      // Only used in sandbox mode
      schemes : [
        {
          columns : 120,
          rows : 100,
          cellSize : 7
        },
        {
          columns : 450,
          rows : 216,
          cellSize : 1
        },
      ],
    },


    // Cell colors
    //
    // dead/trail colors always the same
    // alive color sets are either set by the game (game mode)
    // or set by the user via the schemes (sandbox mode)
    colors : {
      current : 0,
      schedule : false,
      dead: realBackgroundColor,
      trail: grays,
      alive: null,

      // Only used in sandbox mode
      schemes : [
        {
          alive: ['#9963AB', '#E86215'],
          alive_labels: ['Purple', 'Orange'],
        },
        {
          alive: ["#9FE2BF", "#FF1717"],
          alive_labels: ['Green', 'Red'],
        }
      ],
    },


    /**
     * On Load Event
     */
    init : function() {
      try {
        this.listLife.init();   // Reset/init algorithm
        this.loadConfig();      // Load config from URL (autoplay, colors, zoom, ...)
        this.keepDOMElements(); // Keep DOM References (getElementsById)
        this.loadState();       // Load state from URL
        this.canvas.init();     // Init canvas GUI
        this.registerEvents();  // Register event handlers
        this.prepare();
      } catch (e) {
        alert("Error: "+e);
      }
    },


    /**
     * Load config from URL
     *
     * This function is a bit messy, so here's the rundown:
     * - if user provides gameId param, switch to game simulation mode
     *   - get team/map data from games api endpoint
     *   - populate various fields from games api result
     * - if user provides no gameId param, switch to sandbox mode
     *   - if user provides map param, load a map from the maps api endpoint
     *   - if user provides random param, set up state1/state2 to be randomly generated fields
     *   - if user provides s1 or s2 params, set state1/state2 initial conditions
     *   - if user provides nothing, set default state1/state2 params on default map
     */
    loadConfig : function() {
      var grid, zoom;

      // User providing gameId means we go to game mode
      this.gameId = this.helpers.getUrlParameter('gameId');
      if (this.gameId != null) {

        ///////////////////
        // Game simulation mode
        this.game_mode = true;
        this.sandbox_mode = false;

        // Enable map overlay
        this.grid.mapOverlay = true;

        // Get game endpoint and put it in this.gameApiResult
        // this.gameApiResult = json;
        this.gameApiResult = this.defaultGameApiResult;

        // Team names and colors
        this.teamNames = [this.gameApiResult.team1Name, this.gameApiResult.team2Name];
        this.colors.alive = [this.gameApiResult.team1Color, this.gameApiResult.team2Color];

        // Also, store map data as its own variable
        // (useful b/c we may want a map but not in game mode)
        this.mapApiResult = this.gameApiResult.map;

        // Map initial conditions
        this.initialState1 = this.mapApiResult.initialConditions1;
        this.initialState2 = this.mapApiResult.initialConditions2;

        // Map zoom info
        this.columns  = this.mapApiResult.columns;
        this.rows     = this.mapApiResult.rows;
        this.cellSize = this.mapApiResult.cellSize;

      } else {

        // User NOT providing gameId means we go to sandbox mode
        this.mapId = this.helpers.getUrlParameter('mapId');
        this.random = parseInt(this.helpers.getUrlParameter('random'));
        this.s1user = this.helpers.getUrlParameter('s1');
        this.s2user = this.helpers.getUrlParameter('s2');

        ///////////////////
        // Sandbox mode
        this.game_mode = false;
        this.sandbox_mode = true;

        if (this.mapId != null) {
          // Use user-specified map, map's zoom
          // Get map endpoint and put it in this.mapApiResult
          // (for now we just use a dummy default map)
          this.mapApiResult = this.defaultMap;
          // Initial conditions
          this.initialState1 = this.mapApiResult.initialConditions1;
          this.initialState2 = this.mapApiResult.initialConditions2;
          // Zoom info
          this.columns = this.mapApiResult.columns;
          this.rows = this.mapApiResult.rows;
          this.cellSize = this.mapApiResult.cellSize;
          // Enable map overlay
          this.grid.mapOverlay = true;

        } else {
          if (this.random == 1) {
            // Use random map, default zoom
            // Initial conditions
            this.initialState1 = 'random';
            this.initialState2 = 'random';

          } else if ((this.s1user == null) && (this.s2user == null)) {
            // User provided no s1 or s2,
            // so use the default map
            this.initialState1 = this.defaultMap.initialConditions1;
            this.initialState2 = this.defaultMap.initialConditions2;

          } else {
            // User provided s1 or s2
            // If not both, set to [{}] to make program properly skip it
            if (this.s1user != null) {
              this.initialState1 = this.s1user;
            } else {
              this.initialState1 = [{}];
            }
            if (this.s2user != null) {
              this.initialState2 = this.s2user;
            } else {
              this.initialState2 = [{}];
            }
          } // end mapId if/else

          // Parse zoom options and pick out scheme
          zoom = parseInt(this.helpers.getUrlParameter('zoom'), 10);
          if (isNaN(zoom) || zoom < 1 || zoom > GOL.zoom.schemes.length) {
            zoom = 1;
          }
          this.zoom.current = zoom - 1;
          this.columns = this.zoom.schemes[this.zoom.current].columns;
          this.rows = this.zoom.schemes[this.zoom.current].rows;
          this.cellSize = this.zoom.schemes[this.zoom.current].cellSize;

          // Parse color options and pick out scheme
          colorpal = parseInt(this.helpers.getUrlParameter('color'), 10);
          if (isNaN(colorpal) || colorpal < 1 || colorpal > GOL.colors.schemes.length) {
            colorpal = 1;
          }
          this.colors.current = colorpal - 1;
          this.colors.alive = this.colors.schemes[this.colors.current].alive;
          // Replace team names with color labels
          this.teamNames = this.colors.schemes[this.colors.current].alive_labels;
        }
      }

      // Initial grid config
      grid = parseInt(this.helpers.getUrlParameter('grid'), 10);
      if (isNaN(grid) || grid < 1 || grid > this.grid.schemes.length) {
        grid = 1;
      }
      this.grid.current = grid - 1;

      // Add ?autoplay=1 to the end of the URL to enable autoplay
      this.autoplay = this.helpers.getUrlParameter('autoplay') === '1' ? true : this.autoplay;

      // Add ?trail=1 to the end of the URL to show trails
      this.trail.current = this.helpers.getUrlParameter('trail') === '1' ? true : this.trail.current;

    },


    /**
     * Load world state from URL parameter
     * cmr - this is where we use initialState1 and initialState2
     */
    loadState : function() {
      var i, j, y;
      var state1, state2;

      // each stateN is an array of arrays (listlife)
      // stateN[0] is a dictionary:
      //    39: [60]
      // stateN[1] is a dictionary:
      //    40: [62]
      // stateN[2] is a dictionary:
      //    41: [59, 60, 63, 64, 65]

      // state 1 parameter
      //if (true) {
      if (this.initialState1 === 'random') {
        this.randomState(1);
      } else {
        state1 = jsonParse(decodeURI(this.initialState1));
        var irow, icol, y;
        for (irow = 0; irow < state1.length; irow++) {
          for (y in state1[irow]) {
            for (icol = 0 ; icol < state1[irow][y].length ; icol++) {
              var yy = parseInt(y, 10);
              var xx = state1[irow][yy][icol];
              this.listLife.addCell(xx, yy, this.listLife.actualState);
              this.listLife.addCell(xx, yy, this.listLife.actualState1);
            }
          }
        }
      }

      // state 2 parameter
      //if (true) {
      if (this.initialState2 === 'random') {
        this.randomState(2);
      } else {
        state2 = jsonParse(decodeURI(this.initialState2));
        var irow, icol, y;
        for (irow = 0; irow < state2.length; irow++) {
          for (y in state2[irow]) {
            for (icol = 0 ; icol < state2[irow][y].length ; icol++) {
              var yy = parseInt(y, 10);
              var xx = state2[irow][yy][icol];
              this.listLife.addCell(xx, yy, this.listLife.actualState);
              this.listLife.addCell(xx, yy, this.listLife.actualState2);
            }
          }
        }
      }
    },


    /**
     * Create a random pattern
     */
    randomState : function(color) {
      // original pct was 12%, for binary we split 5%
      var i, liveCells = (this.rows * this.columns) * 0.05;

      if (color===0 || color===1) {
        // Color 1
        for (i = 0; i < liveCells; i++) {
          var xx = this.helpers.random(0, this.columns - 1);
          var yy = this.helpers.random(0, this.rows - 1);
          while (this.listLife.isAlive(xx, yy)) {
              xx = this.helpers.random(0, this.columns - 1);
              yy = this.helpers.random(0, this.rows - 1);
          }
          this.listLife.addCell(xx, yy, this.listLife.actualState);
          this.listLife.addCell(xx, yy, this.listLife.actualState1);
        }
      }

      if (color===0 || color===2) {
        // Color 2
        for (i = 0; i < liveCells; i++) {
          var xx = this.helpers.random(0, this.columns - 1);
          var yy = this.helpers.random(0, this.rows - 1);
          while (this.listLife.isAlive(xx, yy)) {
              xx = this.helpers.random(0, this.columns - 1);
              yy = this.helpers.random(0, this.rows - 1);
          }
          this.listLife.addCell(xx, yy, this.listLife.actualState);
          this.listLife.addCell(xx, yy, this.listLife.actualState2);
        }
      }

      //this.listLife.nextGeneration();
    },


    /**
     * Clean up actual state and prepare a new run
     */
    cleanUp : function() {
      this.listLife.init(); // Reset/init algorithm
      this.prepare();
    },


    /**
     * Prepare DOM elements and Canvas for a new run
     */
    prepare : function() {
      this.generation = this.times.algorithm = this.times.gui = 0;
      this.mouseDown = this.clear.schedule = false;

      this.element.generation.innerHTML = '0';

      if (this.game_mode===true) {
        // In game mode, hide controls that the user won't need
        this.element.clearButton.remove();
        this.element.colorButton.remove();
      }

      if (this.grid.mapOverlay===true) {
        this.element.mapName.innerHTML = this.mapApiResult['mapName'];
        this.element.z1lab.innerHTML = this.mapApiResult['mapZone1Name'];
        this.element.z2lab.innerHTML = this.mapApiResult['mapZone2Name'];
        this.element.z3lab.innerHTML = this.mapApiResult['mapZone3Name'];
        this.element.z4lab.innerHTML = this.mapApiResult['mapZone4Name'];
      } else {
        // Remove the Map line from the scoreboard
        this.element.mapScoreboardPanel.remove();
        this.element.z1lab.remove();
        this.element.z2lab.remove();
        this.element.z3lab.remove();
        this.element.z4lab.remove();
      }

      liveCounts = this.getCounts();
      this.element.livecells.innerHTML  = liveCounts[0];
      this.element.livecells1.innerHTML = liveCounts[1];
      this.element.livecells2.innerHTML = liveCounts[2];
      this.element.victory.innerHTML    = liveCounts[3] + "%";
      this.element.coverage.innerHTML   = liveCounts[4] + "%";
      this.element.territory1.innerHTML = liveCounts[5] + "%";
      this.element.territory2.innerHTML = liveCounts[6] + "%";

      // Color any text and populate any team names
      this.updateTeamNamesColors();

      this.canvas.clearWorld(); // Reset GUI
      this.canvas.drawWorld(); // Draw State

      if (this.autoplay) { // Next Flow
        this.autoplay = false;
        this.handlers.buttons.run();
      }
    },

    updateTeamNamesColors : function() {
      var i, e;
      for (i = 0; i < this.element.team1color.length; i++) {
        e = this.element.team1color[i];
        e.style.color = this.colors.alive[0];
      }
      for (i = 0; i < this.element.team2color.length; i++) {
        e = this.element.team2color[i];
        e.style.color = this.colors.alive[1];
      }
      for (i = 0; i < this.element.team1name.length; i++) {
        e = this.element.team1name[i];
        e.innerHTML = this.teamNames[0];
      }
      for (i = 0; i < this.element.team2name.length; i++) {
        e = this.element.team2name[i];
        e.innerHTML = this.teamNames[1];
      }
    },

    getCounts : function() {
      var liveCounts = GOL.listLife.getLiveCounts();
      return liveCounts;
    },

    /**
     * keepDOMElements
     * Save DOM references for this session (one time execution)
     */
    keepDOMElements : function() {
      this.element.generation = document.getElementById('generation');
      this.element.livecells  = document.getElementById('livecells');
      this.element.livecells1 = document.getElementById('livecells1');
      this.element.livecells2 = document.getElementById('livecells2');

      this.element.victory    = document.getElementById('victoryPct');
      this.element.coverage   = document.getElementById('coverage');
      this.element.territory1 = document.getElementById('territory1');
      this.element.territory2 = document.getElementById('territory2');

      this.element.team1color = document.getElementsByClassName("team1color");
      this.element.team1name  = document.getElementsByClassName("team1name");
      this.element.team2color = document.getElementsByClassName("team2color");
      this.element.team2name  = document.getElementsByClassName("team2name");

      this.element.clearButton = document.getElementById('buttonClear');
      this.element.colorButton = document.getElementById('buttonColors');

      this.element.mapName = document.getElementById('mapname-label');
      this.element.mapScoreboardPanel = document.getElementById('scoreboard-panel-map');

      this.element.z1lab = document.getElementById('zone1label');
      this.element.z2lab = document.getElementById('zone2label');
      this.element.z3lab = document.getElementById('zone3label');
      this.element.z4lab = document.getElementById('zone4label');
    },


    /**
     * registerEvents
     * Register event handlers for this session (one time execution)
     */
    registerEvents : function() {

      // Keyboard Events
      this.helpers.registerEvent(document.body, 'keyup', this.handlers.keyboard, false);

      // Controls
      this.helpers.registerEvent(document.getElementById('buttonRun'), 'click', this.handlers.buttons.run, false);
      this.helpers.registerEvent(document.getElementById('buttonStep'), 'click', this.handlers.buttons.step, false);
      this.helpers.registerEvent(document.getElementById('buttonClear'), 'click', this.handlers.buttons.clear, false);

      // Layout
      this.helpers.registerEvent(document.getElementById('buttonTrail'), 'click', this.handlers.buttons.trail, false);
      this.helpers.registerEvent(document.getElementById('buttonGrid'), 'click', this.handlers.buttons.grid, false);
      this.helpers.registerEvent(document.getElementById('buttonColors'), 'click', this.handlers.buttons.colorcycle, false);
    },


    /**
     * Run Next Step
     */
    nextStep : function() {
      var i, x, y, r;
      var liveCellNumbers, liveCellNumber, liveCellNumber1, liveCellNumber2;
      var algorithmTime, guiTime;

      // Algorithm run

      algorithmTime = (new Date());

      liveCounts = GOL.listLife.nextGeneration();

      algorithmTime = (new Date()) - algorithmTime;


      // Canvas run

      guiTime = (new Date());

      for (i = 0; i < GOL.listLife.redrawList.length; i++) {
        x = GOL.listLife.redrawList[i][0];
        y = GOL.listLife.redrawList[i][1];

        if (GOL.listLife.redrawList[i][2] === 1) {
          GOL.canvas.changeCelltoAlive(x, y);
        } else if (GOL.listLife.redrawList[i][2] === 2) {
          GOL.canvas.keepCellAlive(x, y);
        } else {
          GOL.canvas.changeCelltoDead(x, y);
        }
      }

      guiTime = (new Date()) - guiTime;

      // Pos-run updates

      // Clear Trail
      if (GOL.trail.schedule) {
        GOL.trail.schedule = false;
        GOL.canvas.drawWorld();
      }

      // Change Grid
      if (GOL.grid.schedule) {
        GOL.grid.schedule = false;
        GOL.canvas.drawWorld();
      }

      // Change Colors
      if (GOL.colors.schedule) {
        GOL.colors.schedule = false;
        GOL.canvas.drawWorld();
      }

      // Running Information
      GOL.generation++;
      GOL.element.generation.innerHTML = GOL.generation;

      GOL.element.livecells.innerHTML  = liveCounts[0];
      GOL.element.livecells1.innerHTML = liveCounts[1];
      GOL.element.livecells2.innerHTML = liveCounts[2];
      GOL.element.victory.innerHTML    = liveCounts[3] + "%";
      GOL.element.coverage.innerHTML   = liveCounts[4] + "%";
      GOL.element.territory1.innerHTML = liveCounts[5] + "%";
      GOL.element.territory2.innerHTML = liveCounts[6] + "%";

      r = 1.0/GOL.generation;
      GOL.times.algorithm = (GOL.times.algorithm * (1 - r)) + (algorithmTime * r);
      GOL.times.gui = (GOL.times.gui * (1 - r)) + (guiTime * r);

      // Flow Control
      if (GOL.running) {
        window.requestAnimationFrame(GOL.nextStep);
      } else {
        if (GOL.clear.schedule) {
          GOL.cleanUp();
        }
      }
    },


    /** ****************************************************************************************************************************
     * Event Handlers
     */
    handlers : {

      mouseDown : false,
      lastX : 0,
      lastY : 0,


      /**
       * When user clicks down, set mouse down state
       * and change change cell alive/dead state at
       * the current mouse location.
       * (sandbox mode only)
       */
      canvasMouseDown : function(event) {
        if (this.sandbox_mode===true) {
          var position = GOL.helpers.mousePosition(event);
          GOL.canvas.switchCell(position[0], position[1]);
          GOL.handlers.lastX = position[0];
          GOL.handlers.lastY = position[1];
          GOL.handlers.mouseDown = true;
        }
      },


      /**
       * Handle user mouse up instance.
       * (sandbox mode only)
       */
      canvasMouseUp : function() {
        if (this.sandbox_mode===true) {
          GOL.handlers.mouseDown = false;
        }
      },


      /**
       * If we have captured a mouse down event,
       * track where the mouse is going and change
       * cell alive/dead state at mouse location.
       * (sandbox mode only)
       */
      canvasMouseMove : function(event) {
        if (this.sandbox_mode===true) {
          if (GOL.handlers.mouseDown) {
            var position = GOL.helpers.mousePosition(event);
            if ((position[0] !== GOL.handlers.lastX) || (position[1] !== GOL.handlers.lastY)) {
              GOL.canvas.switchCell(position[0], position[1]);
              GOL.handlers.lastX = position[0];
              GOL.handlers.lastY = position[1];
            }
          }
        }
      },


      /**
       * Allow keyboard shortcuts
       */
      keyboard : function(e) {
        var event = e;
        if (!event) {
          event = window.event;
        }

        if (event.keyCode === 67) { // Key: C
          // User can only clear the board in sandbox mode
          if (this.sandbox_mode===true) {
            GOL.handlers.buttons.clear();
          }
        } else if (event.keyCode === 82 ) { // Key: R
          GOL.handlers.buttons.run();
        } else if (event.keyCode === 83 ) { // Key: S
          GOL.handlers.buttons.step();
        }
      },


      buttons : {

        /**
         * Button Handler - Run
         */
        run : function() {

          GOL.running = !GOL.running;
          // Update run/stop button state
          if (GOL.running) {
            GOL.nextStep();
            document.getElementById('buttonRun').textContent = 'Stop';
            document.getElementById('buttonRun').classList.remove("btn-success");
            document.getElementById('buttonRun').classList.add("btn-danger");
          } else {
            document.getElementById('buttonRun').textContent = 'Run';
            document.getElementById('buttonRun').classList.remove("btn-danger");
            document.getElementById('buttonRun').classList.add("btn-success");
          }
        },


        /**
         * Button Handler - Next Step - One Step only
         */
        step : function() {
          if (!GOL.running) {
            GOL.nextStep();
          }
        },


        /**
         * Button Handler - Clear World
         */
        clear : function() {
          if (this.sandbox_mode===true) {
            if (GOL.running) {
              GOL.clear.schedule = true;
              GOL.running = false;
              $("#buttonRun").text("Run");
              document.getElementById('buttonRun').classList.remove("btn-danger");
              document.getElementById('buttonRun').classList.add("btn-success");
            } else {
              GOL.cleanUp();
            }
          }
        },


        /**
         * Button Handler - Remove/Add Trail
         */
        trail : function() {
          //GOL.element.messages.layout.innerHTML = GOL.trail.current ? 'Trail is Off' : 'Trail is On';
          GOL.trail.current = !GOL.trail.current;
          if (GOL.running) {
            GOL.trail.schedule = true;
          } else {
            GOL.canvas.drawWorld();
          }
        },

        /**
         * Cycle through the color schemes
         */
        colorcycle : function() {
          GOL.colors.current = (GOL.colors.current + 1) % GOL.colors.schemes.length;
          GOL.colors.alive = GOL.colors.schemes[GOL.colors.current].alive;
          GOL.teamNames = GOL.colors.schemes[GOL.colors.current].alive_labels;
          GOL.updateTeamNamesColors();
          if (GOL.running) {
            GOL.colors.schedule = true; // Delay redraw
          } else {
            GOL.canvas.drawWorld(); // Force complete redraw
          }
        },

        /**
         * Show/hide the grid
         */
        grid : function() {
          GOL.grid.current = (GOL.grid.current + 1) % GOL.grid.schemes.length;
          if (GOL.running) {
            GOL.grid.schedule = true; // Delay redraw
          } else {
            GOL.canvas.drawWorld(); // Force complete redraw
          }
        },

      },

    },


    /** ****************************************************************************************************************************
     *
     */
    canvas: {

      context : null,
      width : null,
      height : null,
      age : null,
      cellSize : null,
      cellSpace : null,


      /**
       * init
       */
      init : function() {

        this.canvas = document.getElementById('canvas');
        this.context = this.canvas.getContext('2d');

        this.cellSize = GOL.cellSize;
        this.cellSpace = 1;

        // register the mousedown/mouseup/mousemove events with function callbacks
        GOL.helpers.registerEvent(this.canvas, 'mousedown', GOL.handlers.canvasMouseDown, false);
        GOL.helpers.registerEvent(document, 'mouseup', GOL.handlers.canvasMouseUp, false);
        GOL.helpers.registerEvent(this.canvas, 'mousemove', GOL.handlers.canvasMouseMove, false);

        this.clearWorld();
      },


      /**
       * clearWorld
       */
      clearWorld : function () {
        var i, j;

        // Init ages (Canvas reference)
        this.age = [];
        for (i = 0; i < GOL.columns; i++) {
          this.age[i] = [];
          for (j = 0; j < GOL.rows; j++) {
            this.age[i][j] = 0; // Dead
          }
        }
      },


      /**
       * drawWorld
       */
      drawWorld : function() {
        var i, j;

        // Special no grid case
        if (GOL.grid.schemes[GOL.grid.current].color === '') {
          this.setNoGridOn();
          this.width = this.height = 0;
        } else {
          this.setNoGridOff();
          this.width = this.height = 1;
        }

        // Dynamic canvas size
        this.width = this.width + (this.cellSpace * GOL.columns) + (this.cellSize * GOL.columns);
        this.canvas.setAttribute('width', this.width);

        this.height = this.height + (this.cellSpace * GOL.rows) + (this.cellSize * GOL.rows);
        this.canvas.setAttribute('height', this.height);

        // Fill background
        this.context.fillStyle = GOL.grid.schemes[GOL.grid.current].color;
        this.context.fillRect(0, 0, this.width, this.height);


        for (i = 0 ; i < GOL.columns; i++) {
          for (j = 0 ; j < GOL.rows; j++) {
            if (GOL.listLife.isAlive(i, j)) {
              this.drawCell(i, j, true);
            } else {
              this.drawCell(i, j, false);
            }
          }
        }
      },


      /**
       * setNoGridOn
       */
      setNoGridOn : function() {
        this.cellSize = GOL.cellSize + 1;
        this.cellSpace = 0;
      },


      /**
       * setNoGridOff
       */
      setNoGridOff : function() {
        this.cellSize = GOL.cellSize;
        this.cellSpace = 1;
      },


      /**
       * drawCell
       * cmr - this is where we color by color
       */
      drawCell : function (i, j, alive) {

        if (alive) {

          // color by... color
          this.context.fillStyle = GOL.colors.alive[GOL.listLife.getCellColor(i, j) - 1];

        } else {
          if (GOL.trail.current && this.age[i][j] < 0) {
            this.context.fillStyle = GOL.colors.trail[(this.age[i][j] * -1) % GOL.colors.trail.length];
          } else {
            this.context.fillStyle = GOL.colors.dead;
          }
        }

        this.context.fillRect(this.cellSpace + (this.cellSpace * i) + (this.cellSize * i), this.cellSpace + (this.cellSpace * j) + (this.cellSize * j), this.cellSize, this.cellSize);

        // Draw light strokes cutting the canvas through the middle
        if (i===parseInt(GOL.columns/2)) {
          if (GOL.grid.mapOverlay==true) {
            this.context.fillStyle = mapZoneStrokeColor;
            this.context.fillRect(
              (this.cellSpace * i+1) + (this.cellSize * i+1) - 2*this.cellSpace,
              (this.cellSpace * j) + (this.cellSize * j) + this.cellSpace,
              this.cellSpace,
              this.cellSize,
            );
          }
        }

        if (j===parseInt(GOL.rows/2)) {
          if (GOL.grid.mapOverlay==true) {
            this.context.fillStyle = mapZoneStrokeColor;
            console.log('wat');
            this.context.fillRect(
              (this.cellSpace * i+1) + (this.cellSize * i+1) - 2*this.cellSpace,
              (this.cellSpace * j) + (this.cellSize * j) + this.cellSpace,
              this.cellSize,
              this.cellSpace,
            );
          }
        }

      },


      /**
       * switchCell
       * cmr - this is only activated when a user clicks on a cell
       */
      switchCell : function(i, j) {
        if (this.sandbox_mode===true) {
          if (GOL.listLife.isAlive(i, j)) {
            if (GOL.listLife.getCellColor(i, j) == 1) {
              // Swap colors
              GOL.listLife.removeCell(i, j, GOL.listLife.actualState1);
              GOL.listLife.addCell(i, j, GOL.listLife.actualState2);
              this.keepCellAlive(i, j);
            } else {
              GOL.listLife.removeCell(i, j, GOL.listLife.actualState);
              GOL.listLife.removeCell(i, j, GOL.listLife.actualState2);
              this.changeCelltoDead(i, j);
            }
          } else {
            GOL.listLife.addCell(i, j, GOL.listLife.actualState);
            GOL.listLife.addCell(i, j, GOL.listLife.actualState1);
            this.changeCelltoAlive(i, j);
          }
        }
      },


      /**
       * keepCellAlive
       */
      keepCellAlive : function(i, j) {
        if (i >= 0 && i < GOL.columns && j >=0 && j < GOL.rows) {
          this.age[i][j]++;
          this.drawCell(i, j, true);
        }
      },


      /**
       * changeCelltoAlive
       */
      changeCelltoAlive : function(i, j) {
        if (i >= 0 && i < GOL.columns && j >=0 && j < GOL.rows) {
          this.age[i][j] = 1;
          this.drawCell(i, j, true);
        }
      },


      /**
       * changeCelltoDead
       */
      changeCelltoDead : function(i, j) {
        if (i >= 0 && i < GOL.columns && j >=0 && j < GOL.rows) {
          this.age[i][j] = -this.age[i][j]; // Keep trail
          this.drawCell(i, j, false);
        }
      }

    },


    /** ****************************************************************************************************************************
     *
     */
    listLife : {

      actualState : [],
      actualState1 : [],
      actualState2 : [],
      redrawList : [],


      /**
       * Initialize the actual state array (?)
       */
      init : function () {
        this.actualState = [];
      },


      getLiveCounts : function() {
        var i, j;

        var state = GOL.listLife.actualState;
        var liveCells = 0;
        var coverageCells = 0;
        for (i = 0; i < state.length; i++) {
          if ((state[i][0] >= 0) && (state[i][0] < GOL.rows)) {
            for (j = 1; j < state[i].length; j++) {
              if ((state[i][j] >= 0) && (state[i][j] < GOL.columns)) {
                liveCells++;
              }
            }
          }
        }

        var state1 = GOL.listLife.actualState1;
        var liveCells1 = 0;
        for (i = 0; i < state1.length; i++) {
          if ((state1[i][0] >= 0) && (state1[i][0] < GOL.rows)) {
            for (j = 1; j < state1[i].length; j++) {
              if ((state1[i][j] >= 0) && (state1[i][j] < GOL.columns)) {
                liveCells1++;
              }
            }
          }
        }

        var state2 = GOL.listLife.actualState2;
        var liveCells2 = 0;
        for (i = 0; i < state2.length; i++) {
          if ((state2[i][0] >= 0) && (state2[i][0] < GOL.rows)) {
            for (j = 1; j < state2[i].length; j++) {
              if ((state2[i][j] >= 0) && (state2[i][j] < GOL.columns)) {
                liveCells2++;
              }
            }
          }
        }

        var victoryPct;
        if (liveCells1 > liveCells2) {
          victoryPct = liveCells1/(1.0*liveCells1 + liveCells2);
        } else {
          victoryPct = liveCells2/(1.0*liveCells1 + liveCells2);
        }
        victoryPct = (victoryPct * 100).toFixed(1);

        var totalArea = GOL.columns * GOL.rows;
        var coverage = liveCells/(1.0*totalArea);
        coverage = (coverage * 100).toFixed(2);

        var territory1 = liveCells1/(1.0*totalArea);
        territory1 = (territory1 * 100).toFixed(2);
        var territory2 = liveCells2/(1.0*totalArea);
        territory2 = (territory2 * 100).toFixed(2);

        return [
          liveCells,
          liveCells1,
          liveCells2,
          victoryPct,
          coverage,
          territory1,
          territory2
        ];
      },


      nextGeneration : function() {
        var x, y, i, j, m, n, key, t1, t2;
        var alive = 0, alive1 = 0, alive2 = 0;
        var deadNeighbors;
        var newState = [], newState1 = [], newState2 = [];
        var allDeadNeighbors = {};
        var allDeadNeighbors1 = {};
        var allDeadNeighbors2 = {};
        var neighbors, color;
        this.redrawList = [];

        // iterate over each point stored in the actualState list
        for (i = 0; i < this.actualState.length; i++) {
          this.topPointer = 1;
          this.bottomPointer = 1;

          for (j = 1; j < this.actualState[i].length; j++) {
            x = this.actualState[i][j];
            y = this.actualState[i][0];

            // Possible dead neighbors
            deadNeighbors = [[x-1, y-1, 1], [x, y-1, 1], [x+1, y-1, 1], [x-1, y, 1], [x+1, y, 1], [x-1, y+1, 1], [x, y+1, 1], [x+1, y+1, 1]];

            // Get number of live neighbors and remove alive neighbors from deadNeighbors
            result = this.getNeighborsFromAlive(x, y, i, this.actualState, deadNeighbors);
            neighbors = result['neighbors'];
            color = result['color'];

            // Join dead neighbors to check list
            for (m = 0; m < 8; m++) {
              if (deadNeighbors[m] !== undefined) {
                // this cell is dead
                var xx = deadNeighbors[m][0];
                var yy = deadNeighbors[m][1];
                key = xx + ',' + yy; // Create hashtable key

                // count number of dead neighbors
                if (allDeadNeighbors[key] === undefined) {
                  allDeadNeighbors[key] = 1;
                } else {
                  allDeadNeighbors[key]++;
                }
              }
            }

            if (!(neighbors === 0 || neighbors === 1 || neighbors > 3)) {
              this.addCell(x, y, newState);
              if (color==1) {
                this.addCell(x, y, newState1);
              } else if (color==2) {
                this.addCell(x, y, newState2);
              }
              this.redrawList.push([x, y, 2]); // Keep alive
            } else {
              this.redrawList.push([x, y, 0]); // Kill cell
            }
          }
        }

        // Process dead neighbors
        for (key in allDeadNeighbors) {
          if (allDeadNeighbors[key] === 3) {
            // This cell is dead, but has enough neighbors
            // that are alive that it will make new life.
            key = key.split(',');
            t1 = parseInt(key[0], 10);
            t2 = parseInt(key[1], 10);

            // Get color from neighboring parent cells
            color = this.getColorFromAlive(t1, t2);

            this.addCell(t1, t2, newState);
            if (color == 1) {
              this.addCell(t1, t2, newState1);
            } else if (color == 2) {
              this.addCell(t1, t2, newState2);
            }

            this.redrawList.push([t1, t2, 1]);
          }
        }

        this.actualState = newState;
        this.actualState1 = newState1;
        this.actualState2 = newState2;

        return this.getLiveCounts();
      },


      topPointer : 1,
      middlePointer : 1,
      bottomPointer : 1,

      getColorFromAlive : function(x, y) {
        var state1 = this.actualState1;
        var state2 = this.actualState2;

        var color1 = 0;
        var color2 = 0;

        // color1
        for (i = 0; i < state1.length; i++) {
          var yy = state1[i][0];

          if (yy === (y-1)) {
            // Top row
            for (j = 1; j < state1[i].length; j++) {
              var xx = state1[i][j];
              if (xx >= (x-1)) {
                if (xx === (x-1)) {
                  // top left
                  color1++;
                } else if (xx === x) {
                  // top middle
                  color1++;
                } else if (xx === (x+1)) {
                  // top right
                  color1++;
                }
              }
              if (xx >= (x+1)) {
                break;
              }
            }

          } else if (yy === y) {
            // Middle row
            for (j = 1; j < state1[i].length; j++) {
              var xx = state1[i][j];
              if (xx >= (x-1)) {
                if (xx === (x-1)) {
                  // top left
                  color1++;
                } else if (xx === (x+1)) {
                  // top right
                  color1++;
                }
              }
              if (xx >= (x+1)) {
                break;
              }
            }

          } else if (yy === (y+1)) {
            // Bottom row
            for (j = 1; j < state1[i].length; j++) {
              var xx = state1[i][j];
              if (xx >= (x-1)) {
                if (xx === (x-1)) {
                  // bottom left
                  color1++;
                } else if (xx === x) {
                  // bottom middle
                  color1++;
                } else if (xx === (x+1)) {
                  // bottom right
                  color1++;
                }
              }
              if (xx >= (x+1)) {
                break;
              }
            }
          }
        }

        // color2
        for (i = 0; i < state2.length; i++) {
          var yy = state2[i][0];

          if (yy === (y-1)) {
            // Top row
            for (j = 1; j < state2[i].length; j++) {
              var xx = state2[i][j];
              if (xx >= (x-1)) {
                if (xx === (x-1)) {
                  // top left
                  color2++;
                } else if (xx === x) {
                  // top middle
                  color2++;
                } else if (xx === (x+1)) {
                  // top right
                  color2++;
                }
              }
              if (xx >= (x+1)) {
                break;
              }
            }

          } else if (yy === y) {
            // Middle row
            for (j = 1; j < state2[i].length; j++) {
              var xx = state2[i][j];
              if (xx >= (x-1)) {
                if (xx === (x-1)) {
                  // left
                  color2++;
                } else if (xx === (x+1)) {
                  // right
                  color2++;
                }
              }
              if (xx >= (x+1)) {
                break;
              }
            }

          } else if (yy === (y+1)) {
            // Bottom row
            for (j = 1; j < state2[i].length; j++) {
              var xx = state2[i][j];
              if (xx >= (x-1)) {
                if (xx === (x-1)) {
                  // bottom left
                  color2++;
                } else if (xx === x) {
                  // bottom middle
                  color2++;
                } else if (xx === (x+1)) {
                  // bottom right
                  color2++;
                }
              }
              if (xx >= (x+1)) {
                break;
              }
            }
          }
        }

        if (color1 > color2) {
          return 1;
        } else if (color1 < color2) {
          return 2;
        } else {
          return 0;
        }
      },

      /**
       *
       */
      getNeighborsFromAlive : function (x, y, i, state, possibleNeighborsList) {
        var neighbors = 0, k;
        var neighbors1 = 0, neighbors2 = 0;

        // Top
        if (state[i-1] !== undefined) {
          if (state[i-1][0] === (y - 1)) {
            for (k = this.topPointer; k < state[i-1].length; k++) {

              if (state[i-1][k] >= (x-1) ) {

                if (state[i-1][k] === (x - 1)) {
                  possibleNeighborsList[0] = undefined;
                  this.topPointer = k + 1;
                  neighbors++;
                  var xx = state[i-1][k];
                  var yy = state[i-1][0];
                  if (this.getCellColor(xx, yy) == 1) {
                    neighbors1++;
                  }
                  if (this.getCellColor(xx, yy) == 2) {
                    neighbors2++;
                  }
                }

                if (state[i-1][k] === x) {
                  possibleNeighborsList[1] = undefined;
                  this.topPointer = k;
                  neighbors++;
                  var xx = state[i-1][k];
                  var yy = state[i-1][0];
                  if (this.getCellColor(xx, yy) == 1) {
                    neighbors1++;
                  }
                  if (this.getCellColor(xx, yy) == 2) {
                    neighbors2++;
                  }
                }

                if (state[i-1][k] === (x + 1)) {
                  possibleNeighborsList[2] = undefined;

                  if (k == 1) {
                    this.topPointer = 1;
                  } else {
                    this.topPointer = k - 1;
                  }

                  neighbors++;
                  var xx = state[i-1][k];
                  var yy = state[i-1][0];
                  if (this.getCellColor(xx, yy) == 1) {
                    neighbors1++;
                  }
                  if (this.getCellColor(xx, yy) == 2) {
                    neighbors2++;
                  }
                }

                if (state[i-1][k] > (x + 1)) {
                  break;
                }
              }
            }
          }
        }

        // Middle
        for (k = 1; k < state[i].length; k++) {
          if (state[i][k] >= (x - 1)) {

            if (state[i][k] === (x - 1)) {
              possibleNeighborsList[3] = undefined;
              neighbors++;
              var xx = state[i][k];
              var yy = state[i][0];
              if (this.getCellColor(xx, yy) == 1) {
                neighbors1++;
              }
              if (this.getCellColor(xx, yy) == 2) {
                neighbors2++;
              }
            }

            if (state[i][k] === (x + 1)) {
              possibleNeighborsList[4] = undefined;
              neighbors++;
              var xx = state[i][k];
              var yy = state[i][0];
              if (this.getCellColor(xx, yy) == 1) {
                neighbors1++;
              }
              if (this.getCellColor(xx, yy) == 2) {
                neighbors2++;
              }
            }

            if (state[i][k] > (x + 1)) {
              break;
            }
          }
        }

        // Bottom
        if (state[i+1] !== undefined) {
          if (state[i+1][0] === (y + 1)) {
            for (k = this.bottomPointer; k < state[i+1].length; k++) {
              if (state[i+1][k] >= (x - 1)) {

                if (state[i+1][k] === (x - 1)) {
                  possibleNeighborsList[5] = undefined;
                  this.bottomPointer = k + 1;
                  neighbors++;
                  var xx = state[i+1][k];
                  var yy = state[i+1][0];
                  if (this.getCellColor(xx, yy) == 1) {
                    neighbors1++;
                  }
                  if (this.getCellColor(xx, yy) == 2) {
                    neighbors2++;
                  }
                }

                if (state[i+1][k] === x) {
                  possibleNeighborsList[6] = undefined;
                  this.bottomPointer = k;
                  neighbors++;
                  var xx = state[i+1][k];
                  var yy = state[i+1][0];
                  if (this.getCellColor(xx, yy) == 1) {
                    neighbors1++;
                  }
                  if (this.getCellColor(xx, yy) == 2) {
                    neighbors2++;
                  }
                }

                if (state[i+1][k] === (x + 1)) {
                  possibleNeighborsList[7] = undefined;

                  if (k == 1) {
                    this.bottomPointer = 1;
                  } else {
                    this.bottomPointer = k - 1;
                  }

                  neighbors++;
                  var xx = state[i+1][k];
                  var yy = state[i+1][0];
                  if (this.getCellColor(xx, yy) == 1) {
                    neighbors1++;
                  }
                  if (this.getCellColor(xx, yy) == 2) {
                    neighbors2++;
                  }
                }

                if (state[i+1][k] > (x + 1)) {
                  break;
                }
              }
            }
          }
        }

        var color;
        if (neighbors1 >= neighbors2) {
          color = 1;
        } else {
          color = 2;
        }

        //return neighbors;
        return {
          neighbors: neighbors,
          color: color
        }
      },


      /**
       * Check if the cell at location (x, y) is alive
       */
      isAlive : function(x, y) {
        var i, j;

        for (i = 0; i < this.actualState.length; i++) {
          // check that first coordinate in actualState matches
          if (this.actualState[i][0] === y) {
            for (j = 1; j < this.actualState[i].length; j++) {
              // check that second coordinate in actualState matches
              if (this.actualState[i][j] === x) {
                return true;
              }
            }
          }
        }
        return false;
      },

      /**
       * Get the color of the cell at location (x, y)
       */
      getCellColor : function(x, y) {

        for (i = 0; i < this.actualState1.length; i++) {
          if (this.actualState1[i][0] === y) {
            for (j = 1; j < this.actualState1[i].length; j++) {
              if (this.actualState1[i][j] === x) {
                return 1;
              }
            }
          }
        }
        for (i = 0; i < this.actualState2.length; i++) {
          if (this.actualState2[i][0] === y) {
            for (j = 1; j < this.actualState2[i].length; j++) {
              if (this.actualState2[i][j] === x) {
                return 2;
              }
            }
          }
        }
        return 0;
      },

      /**
       *
       */
      removeCell : function(x, y, state) {
        var i, j;

        for (i = 0; i < state.length; i++) {
          if (state[i][0] === y) {

            if (state[i].length === 2) { // Remove all Row
              state.splice(i, 1);
            } else { // Remove Element
              for (j = 1; j < state[i].length; j++) {
                if (state[i][j] === x) {
                  state[i].splice(j, 1);
                }
              }
            }
          }
        }
      },


      /**
       *
       */
      addCell : function(x, y, state) {
        if (state.length === 0) {
          state.push([y, x]);
          return;
        }

        var k, n, m, tempRow, newState = [], added;

        // figure out where in the list to insert the new cell
        if (y < state[0][0]) {
          // handle case of y < any other y, so add to beginning of list

          // set first element of newState and bump everybody else by 1
          newState = [[y,x]];
          for (k = 0; k < state.length; k++) {
            newState[k+1] = state[k];
          }

          // copy newState to state
          for (k = 0; k < newState.length; k++) {
            state[k] = newState[k];
          }

          return;

        } else if (y > state[state.length - 1][0]) {
          // handle case of y > any other y, so add to end
          state[state.length] = [y, x];
          return;

        } else { // Add to Middle

          for (n = 0; n < state.length; n++) {
            if (state[n][0] === y) { // Level Exists
              tempRow = [];
              added = false;
              for (m = 1; m < state[n].length; m++) {
                if ((!added) && (x < state[n][m])) {
                  tempRow.push(x);
                  added = !added;
                }
                tempRow.push(state[n][m]);
              }
              tempRow.unshift(y);
              if (!added) {
                tempRow.push(x);
              }
              state[n] = tempRow;
              return;
            }

            if (y < state[n][0]) { // Create Level
              newState = [];
              for (k = 0; k < state.length; k++) {
                if (k === n) {
                  newState[k] = [y,x];
                  newState[k+1] = state[k];
                } else if (k < n) {
                  newState[k] = state[k];
                } else if (k > n) {
                  newState[k+1] = state[k];
                }
              }

              for (k = 0; k < newState.length; k++) {
                state[k] = newState[k];
              }

              return;
            }
          }
        }
      }

    },


    /** ****************************************************************************************************************************
     *
     */
    helpers : {
      urlParameters : null, // Cache


      /**
       * Return a random integer from [min, max]
       */
      random : function(min, max) {
        return min <= max ? min + Math.round(Math.random() * (max - min)) : null;
      },


      /**
       * Get URL Parameters
       */
      getUrlParameter : function(name) {
        if (this.urlParameters === null) { // Cache miss
          var hash, hashes, i;

          this.urlParameters = [];
          hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');

          for (i = 0; i < hashes.length; i++) {
            hash = hashes[i].split('=');
            this.urlParameters.push(hash[0]);
            this.urlParameters[hash[0]] = hash[1];
          }
        }

        return this.urlParameters[name];
      },


      /**
       * Register Event
       */
      registerEvent : function (element, event, handler, capture) {
        if (/msie/i.test(navigator.userAgent)) {
          element.attachEvent('on' + event, handler);
        } else {
          element.addEventListener(event, handler, capture);
        }
      },


      /**
       *
       */
      mousePosition : function (e) {
        // http://www.malleus.de/FAQ/getImgMousePos.html
        // http://www.quirksmode.org/js/events_properties.html#position
        var event, x, y, domObject, posx = 0, posy = 0, top = 0, left = 0, cellSize = GOL.cellSize + 1;

        event = e;
        if (!event) {
          event = window.event;
        }

        if (event.pageX || event.pageY)     {
          posx = event.pageX;
          posy = event.pageY;
        } else if (event.clientX || event.clientY)  {
          posx = event.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
          posy = event.clientY + document.body.scrollTop + document.documentElement.scrollTop;
        }

        domObject = event.target || event.srcElement;

        while ( domObject.offsetParent ) {
          left += domObject.offsetLeft;
          top += domObject.offsetTop;
          domObject = domObject.offsetParent;
        }

        domObject.pageTop = top;
        domObject.pageLeft = left;

        x = Math.ceil(((posx - domObject.pageLeft)/cellSize) - 1);
        y = Math.ceil(((posy - domObject.pageTop)/cellSize) - 1);

        return [x, y];
      }
    }

  };


  /**
   * Init on 'load' event
   */
  GOL.helpers.registerEvent(window, 'load', function () {
    GOL.init();
  }, false);

}());
