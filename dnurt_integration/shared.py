from multiprocessing import Array as MArray
# Shared array for multiprocessing
# 0, 1, 6 - scopus.
    # 6 - num of valid authors.
    # 1 - total num of authors
    # 0 - current author index
# 2, 3 - wos
# 4, 5 - gscholar
updating_status = MArray('i', 7)
