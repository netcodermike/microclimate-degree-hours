import math

def analyze(data):
    base, samples = data["base"], data["samples"]
    if not math.isfinite(base) or len(samples) < 2:
        raise ValueError("A finite threshold and two samples are required")
    intervals = []
    for (start, before), (end, after) in zip(samples, samples[1:]):
        width = end - start
        if width <= 0 or not all(map(math.isfinite,(before,after,width))):
            raise ValueError("Sample times must strictly increase and values must be finite")
        a, b = before-base, after-base
        low, high = sorted((a,b))
        if high <= 0:
            area = 0
        elif low >= 0:
            area = width * (low+high) / 2
        else:
            area = width * high**2 / (high-low) / 2
        intervals.append(area)
    return {"degree_hours":round(sum(intervals),6),"intervals":[round(a,6) for a in intervals]}

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
