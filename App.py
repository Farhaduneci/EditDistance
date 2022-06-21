import numpy as np

SUBSTITUTION_COST = 2
INSERTION_COST = 1
DELETION_COST = 1


def min_cost_path(cost, operations):
    # operation at the last cell
    path = [operations[cost.shape[0] - 1][cost.shape[1] - 1]]

    row = cost.shape[0] - 1
    col = cost.shape[1] - 1

    while row > 0 and col > 0:
        if cost[row - 1][col - 1] <= cost[row - 1][col] and cost[row - 1][col - 1] <= cost[row][col - 1]:
            path.append(operations[row - 1][col - 1])
            row -= 1
            col -= 1
        elif cost[row - 1][col] <= cost[row - 1][col - 1] and cost[row - 1][col] <= cost[row][col - 1]:
            path.append(operations[row - 1][col])
            row -= 1
        else:
            path.append(operations[row][col - 1])
            col -= 1

    return "".join(path[::-1][1:])


def edit_distance_dp(seq1, seq2):
    # create an empty 2D matrix to store cost
    cost = np.zeros((len(seq1) + 1, len(seq2) + 1))

    # fill the first row and column with 0
    for i in range(len(seq1) + 1):
        cost[i][0] = i

    for j in range(len(seq2) + 1):
        cost[0][j] = j

    # to store the operations made
    operations = np.asarray([['-' for j in range(len(seq2) + 1)]
                            for i in range(len(seq1) + 1)])

    # fill the first row by insertion
    for i in range(1, len(seq1) + 1):
        cost[i][0] = cost[i - 1][0] + INSERTION_COST
        operations[i][0] = 'I'

    # fill the first column by insertion operation (D)
    for j in range(1, len(seq2) + 1):
        cost[0][j] = cost[0][j - 1] + INSERTION_COST
        operations[0][j] = 'D'

    operations[0, 0] = '-'

    # now, iterate over each row and column
    for row in range(1, len(seq1) + 1):
        for col in range(1, len(seq2) + 1):

            # if both the characters are same then the cost will be same as
            # the cost of the previous sub-sequence
            if seq1[row - 1] == seq2[col - 1]:
                cost[row][col] = cost[row - 1][col - 1]
            else:
                insertion_cost = cost[row][col - 1] + INSERTION_COST
                deletion_cost = cost[row - 1][col] + DELETION_COST
                substitution_cost = cost[row - 1][col - 1] + SUBSTITUTION_COST

                # calculate the minimum cost
                cost[row][col] = min(
                    insertion_cost, deletion_cost, substitution_cost)

                # get the operation
                if cost[row][col] == substitution_cost:
                    operations[row][col] = 'S'

                elif cost[row][col] == INSERTION_COST:
                    operations[row][col] = 'I'
                else:
                    operations[row][col] = 'D'

    return cost[len(seq1), len(seq2)], min_cost_path(cost, operations)


def main():
    start_string = input("Enter Start String: ")
    end_string = input("Enter Ending String: ")

    score, operations = edit_distance_dp(start_string, end_string)

    print(
        f"Edit Distance between `{start_string}` and `{end_string}` is: {int(score)}")

    OPERATIONS_MAPPING = {
        '-': 'No Operation',
        'S': 'Substitution',
        'I': 'Insertion',
        'D': 'Deletion'
    }

    print("\nOperations performed are:")
    print(" Operations on Start String:")
    for char, operation in zip(start_string, operations):
        print(f"   Char '{char}' -> {OPERATIONS_MAPPING[operation]}")

    print("\n Operations on Ending String:")
    for char, operation in zip(end_string, operations):
        print(f"   Char '{char}' -> {OPERATIONS_MAPPING[operation]}")


if __name__ == "__main__":
    main()
