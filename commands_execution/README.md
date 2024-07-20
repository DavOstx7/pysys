# Packages Explanation:

* commands -> contains command types: command types store the commands and their details.
* commands_structures -> contains complicated commands types named "commands_structures": command structure types
  contain multiple commands that have a flow between them.
* executables -> contains executable types: executable types contain a description for executable environment.
* processable -> contains processable types: processable types contain executable for execution, and either a command
  type or command structure type to be executed.

# Developer Executor

* made for other developers' library's to use
* uses the correct syntax for executing command
* capable to be wrapped for easier use

# Executor

* made for users to use in projects
* executes the processable types
* cannot execute multiple processable types (if desired, the programmer needs to design his code so that he can loop
  through multiple executable types and store their output)
* in order to add to the executor, new functions will be needed (either via inheritacne or code change)