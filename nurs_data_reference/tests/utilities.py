import os

import pandas as pd
import numpy as np

column_name = lambda: "".join(np.random.choice(list("ABCDE"), 5))


def fake_data(k, p):
    return pd.DataFrame(
        np.random.choice(list("ABCDE"), [p, k]),
        columns=[column_name() for _ in range(k)]
    )


if __name__ == '__main__':
    data = pd.DataFrame({
        "Col 1": np.random.choice(list("ABCDE"), 50),
        "Col 2": np.random.choice(list("AAAAABCDE"), 50),
        "Col 3": np.random.choice(list("ABBBBBCDDDDE"), 50)
    })

    data.to_csv("test_files/example_data.csv", index=False)

    file_path = "test_files"
    for dir in ["spider_folder", "spider_folder/first_layer",
                "spider_folder/first_layer/second_layer"]:
        for i in range(2):
            fake_data(50, 500).to_csv(os.path.join(file_path, dir, f"file {i}.csv"), index=False)
        for i in range(2):
            fake_data(50, 500).to_excel(os.path.join(file_path, dir, f"Data.xlsx"),
                                  index=False, sheet_name=f"Sheet {i}")
