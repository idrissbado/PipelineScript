"""
Final Complete Test - PipelineScript
====================================
"""

print("=" * 70)
print("PIPELINESCRIPT - FINAL COMPLETE TEST")
print("=" * 70)

from pipelinescript import run, Pipeline

# Test with correct pipeline
print("\n[FULL PIPELINE TEST]")
print("-" * 70)

script = """
load examples/iris.csv
clean missing
encode
split 80/20 --target species
train random_forest
evaluate
"""

print("Script:")
print(script)
print("-" * 70)

result = run(script)

if result.success:
    print(f"\n✅ SUCCESS! Pipeline completed in {result.duration:.2f}s\n")
    
    print("📊 Results:")
    print(f"   Model: {type(result.context.model).__name__}")
    
    if result.context.metrics:
        print("\n   Metrics:")
        for key, value in result.context.metrics.items():
            if key != 'report' and isinstance(value, (int, float)):
                print(f"      • {key}: {value:.4f}")
    
    print("\n   Execution Log:")
    for entry in result.context.log:
        print(f"      • {entry}")
    
    print("\n" + "=" * 70)
    print("🔥 PIPELINESCRIPT IS WORKING PERFECTLY!")
    print("=" * 70)
    print("\n✅ READY FOR PyPI PUBLICATION!")
    
else:
    print(f"\n❌ Failed: {result.error}")
