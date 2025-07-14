const vm = require('vm');
const ctx = require('ctx-module').makeNodeProgramContext();

vm.runInContext('require("dcp-client").init()', ctx).then(console.log('initialized dcp-client'));