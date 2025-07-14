python.exec(`
import pythonmonkey
import sys
import os
import inspect
`);

process.argv0 = python.eval('sys.executable');
process.argv = [ process.argv0 ].concat(python.eval('sys.argv'));
process.exit = function pm$$processExit(exitCode) {
if (arguments.length === 0)
  exitCode = process.exitCode;
if (typeof exitCode !== 'number')
  exitCode = !exitCode ? 0 : parseInt(exitCode) || 1;
python.eval('lambda x: exit(int(x))')(exitCode & 255);
};