import argparse
import re

def process_log(log):
    debugs = find_debugs(log)
    debug_goals = find_goals(debugs)
    for goal_num in range(len(debug_goals)):
        debug_goal = debug_goals[goal_num]
        first_line = first_meaningful_line(debug_goal)
        looking_for = last_looking_for(debug_goal[:first_line])
        print("Goal %d, %d Lines:" % (goal_num + 1, len(debug_goal)))
        print("   " + looking_for)

# Get all the debug lines out of the file
def find_debugs(log):
    debugs = []
    cur_line = ""

    for line in log:
        line = line.replace('\r', '').replace('\n', '')
        if line.startswith("Debug:"):
            if cur_line:
                debugs.append(cur_line)
            cur_line = line
        else:
            if cur_line:
                cur_line += " " + line.strip()
    debugs.append(cur_line)
    return debugs

# Return a list of all the debug statements for each numbered goal
def find_goals(debugs):
    goal_chunks = []
    cur_goal = 1
    cur_chunk = []

    for debug in debugs:
        goal_num = get_goal_num(debug)
        if goal_num > cur_goal:
            goal_chunks.append(cur_chunk)
            cur_goal = goal_num
            cur_chunk = [debug]
        else:
            cur_chunk.append(debug)
    goal_chunks.append(cur_chunk)
    return goal_chunks

def get_goal_num(debug):
    matchObj = re.match("Debug: ([0-9]+)(\.|:)", debug)
    return int(matchObj.group(1))

# Look for the first thing that is not a looking for or a partial_application_tactic
def first_meaningful_line(debug_goal):
    for line_num in range(len(debug_goal)):
        line = debug_goal[line_num]
        if not "looking for" in line and \
           not "partial_application_tactic" in line and \
           not "no match for" in line and \
           not re.search("Debug: .* : \(", line) and \
           not "(*external*)" in line:
            return line_num

# Look for the last looking for
def last_looking_for(debugs):
    for debug in reversed(debugs):
        searchObj = re.search("looking for \((.*)\)", debug)
        if searchObj:
            return searchObj.group(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', "--filename", required=True)
    args = parser.parse_args()
    with open(args.filename) as f:
        log = f.readlines()
    process_log(log)

if __name__ == "__main__":
    main()
