'''
TO-DO List
- make the plot hold at the end for the user to analyze
- introduce a bit of OOP to make code easier to read/update
    - one way of doing this could be for getting the functions from the
    algorithms py
- refactor code
    - come up with better variable names
    - comment certain things
- make the program terminate and report fatal error if functions take different
number of inputs
- create readme file
- make other checks to make sure the user didn't screw up?
- make the program more flexible:
    - works for comparing functions that take in objects other than just lists
    as objects
    - give option to modify the generate random list option:
        -switch from ordered to random to something else
        -provide their own inputs
 - AppleScript or simple app that takes a drag and drop algorithms.py or .txt
 file to trigger all the functionality
- Time complexity detection
    - Scipy module that finds polynomial variables
        - Try log n, n, n log n, n^x, x^n, x! and choose the one that can find
        the closest root mean square
    - Machine learning
        - CNN of graph image?
        - Logistic regression?
    - Anything more simple?
- Size complexity detection
- Function picker that optimized for a certain n size or storage size or
scalability or compromise thereof
- Check returns of the functions to make sure they are equal. Raise error if
not
- Spit out time estimates in the verbosity section. Don’t forget to deduct the
overhead of calling timeit and (especially) lambda
    - Verify that lambda takes the same amount of time regardless of which
    function it takes ( in the context of this application, of course)
- Incorporate unit testing. Use Pytest?
- Try to use lambdas, list comprehensions, and decorators as much as possible
- Use something more sophisticated than Matplotlib (like Seaborn) and maybe
also make it interactive
- Use faker for other use case data generators?
- Add a feature to calculate average time, worst-case time, and best-case time.
Also maybe add a feature which iterates over a new input to find max time and
min time – trying to make them reach extremes to get a full sense of the
spectrum
-  Add a feature that plays around with input type of similar style such as
array vs linked lists for a list type of input. This is to see how different
data structures affect the time & space complexity. Could propose improvements
to user
- Either replace functionality or add option to switch to loafing a .txt or .py
file that is passed as an argument through the CLI instead of importing the
algorithms.py library. This probably increases flexibility for users and
adaptability for future expansions (to AppleScript or web app)
- Use mypy to check function input and output types. Based off this, we can:
    - Raise exceptions if the compared functions don’t match
    - Generate specialized random inputs based on detected types
- If type annotations not used, ask user to input some details about
application
- ^ actually, can’t we just use .istype?
- Make it possible for the user to specify the file name (maybe even full
path?) to be used through argparse. 
 - turn into a web app?!
'''


import random
import timeit
import time
import matplotlib.pyplot as plt
import argparse
from inspect import getmembers, isfunction, signature
import algorithms


def random_list_generator(n):
    random_list = random.sample(range(n * 10), n)
    random_list.sort()

    return random_list


def main():

    parser = argparse.ArgumentParser(description="bigOviz")
    parser.add_argument('--reps',
                        nargs='?', default=2, type=int,
                        help="set the number of times to repeat each \
                        algorithm for the given input size")
    parser.add_argument('--max_time_per_loop',
                        nargs='?', default=2, type=float,
                        help="set the max time the program is allowed to run \
                        per input size increment before prompting user for \
                        instruction to continue or quit")
    parser.add_argument('--n_initial',
                        nargs='?', default=1, type=int,
                        help="set input size to start with")
    parser.add_argument('--n_max',
                        nargs='?', default=10, type=int,
                        help="set input size to end with")
    parser.add_argument('--n_increment',
                        nargs='?', default=1, type=int,
                        help="set input size increment")
    # need to verify logic for this feature and clarify!
    parser.add_argument('-p', '--pause_for_user_input',
                        action='store_false',
                        help="select this option to be prompted whether or \
                        not the program should continue once increment loops \
                        have reached the max_time_per_loop")
    # add more info to the verbose option? function results?
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help="prints algorithm function names to the CLI")
    args = parser.parse_args()

    reps = args.reps
    max_time_per_loop = args.max_time_per_loop
    n_initial = args.n_initial
    n_max = args.n_max
    n_increment = args.n_increment
    pause_for_user_input = args.pause_for_user_input

    func_list = [o[0] for o in getmembers(algorithms) if isfunction(o[1])]

    if args.verbose:
        print("performing analysis on the following functions:")
        for func in func_list:
            print('    - {}'.format(func))

    testRange = range(n_initial, n_max, n_increment)

    # how many lists are required as inputs?
    qty_list_inputs = len(
        signature(getattr(algorithms, func_list[0])).parameters)

    # check to see if all functions take same number of inputs
    for func in func_list[1:]:
        input_check = len(signature(getattr(algorithms, func)).parameters)
        if input_check != qty_list_inputs:
            print("This is an error message!")

    # initialize plot
    plt.interactive(True)
    func_line_colors = []
    for i in range(len(func_list)):
        # dummy point out of range just to get the legend to work)
        plot_line, = plt.plot(-1, -1, '-', label=func_list[i])
        func_line_colors.append(plot_line.get_c())
    plt.legend()
    plt.ylabel('average execution time')
    plt.xlabel("starting input size 'n' ")

    func_list_results = []
    for _ in func_list:
        func_list_results.append([])

    for n in testRange:
        loop_start_time = time.time()
        random_lists = [random_list_generator(
            n) for random_list in range(qty_list_inputs)]

        for i in range(len(func_list_results)):
            func_list_results[i].append(timeit.timeit(lambda: getattr(
                algorithms, func_list[i])(*random_lists), number=reps) / reps)
        loop_end_time = time.time()
        loop_time = loop_end_time - loop_start_time

        for i in range(len(func_list_results)):
            plt.plot(testRange[:testRange.index(n) + 1],
                     func_list_results[i], color=func_line_colors[i])

        x_max = max(testRange)
        y_max = max([max(func_results) for func_results in func_list_results])
        plt.axis([0, x_max, 0, y_max])
        plt.show()
        plt.pause(0.05)

        if loop_time > max_time_per_loop and pause_for_user_input is False:
            pause_for_user_input -= 1  # need comment to explain this fuckery
            time_limit_prompt = "\n" +\
                                "New iterations are now taking over {}" +\
                                " seconds to complete."
            print(time_limit_prompt.format(max_time_per_loop))
            print(
                "Want to continue?\n"
                "    y: yes, continue until the end\n",
                "   n: no, quit",
            )

            while True:
                pause_for_user_input = input()
                if pause_for_user_input in ("y", "n"):
                    break

            if pause_for_user_input == "y":
                pause_for_user_input = True
                print("resuming...")
                continue
            elif pause_for_user_input == "n":
                quit()

    print("done!")
    plt.pause(1000)


if __name__ == "__main__":
    main()
