from typing import Any, Callable


class Test:
    def __init__(self, *test_cases: tuple[dict, Any]) -> None:
        self.test_cases = test_cases
        self.results = dict()
        
    def __call__(self, f: Callable) -> Any:
        for i, (input, expected) in enumerate(self.test_cases):
            if f(**input) == expected:
                self.results[i] = True
            else:
                self.results[i] = False
                
        if all(v for k, v in self.results.items()):
            print("All tests passed")
