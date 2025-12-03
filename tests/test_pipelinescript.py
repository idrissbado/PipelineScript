"""
PipelineScript Tests
====================

Comprehensive test suite for PipelineScript functionality.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path

# Import PipelineScript modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from pipelinescript import run, parse, compile, Pipeline
from pipelinescript.parser import PipelineParser, PipelineLexer
from pipelinescript.compiler import PipelineCompiler
from pipelinescript.executor import PipelineExecutor
from pipelinescript.pipeline import quick_classification


class TestParser:
    """Test parser functionality."""
    
    def test_lexer_tokenize(self):
        """Test lexical analysis."""
        lexer = PipelineLexer()
        tokens = lexer.tokenize("load data.csv")
        
        assert len(tokens) == 3  # command + path + EOF
        assert tokens[0].value == "load"
        assert tokens[1].value == "data.csv"
    
    def test_parser_simple(self):
        """Test simple parsing."""
        parser = PipelineParser()
        ast = parser.parse("load data.csv\nclean missing")
        
        assert len(ast) == 2
        assert ast[0].command == "load"
        assert ast[0].args == ["data.csv"]
        assert ast[1].command == "clean"
        assert ast[1].args == ["missing"]
    
    def test_parser_with_options(self):
        """Test parsing with options."""
        parser = PipelineParser()
        ast = parser.parse("split 80/20 --target label")
        
        assert len(ast) == 1
        assert ast[0].command == "split"
        assert "target" in ast[0].options
        assert ast[0].options["target"] == "label"
    
    def test_parser_comments(self):
        """Test comment handling."""
        parser = PipelineParser()
        ast = parser.parse("""
            # Load data
            load data.csv
            # Clean it
            clean missing
        """)
        
        assert len(ast) == 2


class TestCompiler:
    """Test compiler functionality."""
    
    def test_compile_load(self):
        """Test load command compilation."""
        parser = PipelineParser()
        ast = parser.parse("load data.csv")
        
        compiler = PipelineCompiler()
        steps = compiler.compile(ast)
        
        assert len(steps) == 1
        assert steps[0].name == "load"
    
    def test_compile_pipeline(self):
        """Test full pipeline compilation."""
        parser = PipelineParser()
        ast = parser.parse("""
            load data.csv
            clean missing
            split 80/20
            train xgboost
        """)
        
        compiler = PipelineCompiler()
        steps = compiler.compile(ast)
        
        assert len(steps) == 4
        assert steps[0].name == "load"
        assert steps[1].name == "clean"
        assert steps[2].name == "split"
        assert steps[3].name == "train"


class TestExecutor:
    """Test executor functionality."""
    
    def test_execution_context(self):
        """Test execution context."""
        from pipelinescript.executor import ExecutionContext
        
        context = ExecutionContext()
        context['data'] = pd.DataFrame({'a': [1, 2, 3]})
        
        assert context['data'] is not None
        assert len(context['data']) == 3


class TestPipeline:
    """Test high-level Pipeline API."""
    
    def test_pipeline_creation(self):
        """Test pipeline creation."""
        pipeline = Pipeline()
        
        pipeline.load("data.csv")
        pipeline.clean_missing()
        pipeline.split(0.8)
        
        script = pipeline.get_script()
        
        assert "load data.csv" in script
        assert "clean missing" in script
        assert "split" in script
    
    def test_pipeline_chaining(self):
        """Test method chaining."""
        pipeline = (Pipeline()
            .load("data.csv")
            .clean_missing()
            .encode()
            .split(0.8)
        )
        
        script = pipeline.get_script()
        lines = script.split('\n')
        
        assert len(lines) == 4


class TestIntegration:
    """Integration tests with real data."""
    
    @pytest.fixture
    def sample_data(self, tmp_path):
        """Create sample CSV file."""
        data = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100),
            'feature3': np.random.randn(100),
            'target': np.random.choice([0, 1], 100)
        })
        
        filepath = tmp_path / "test_data.csv"
        data.to_csv(filepath, index=False)
        
        return str(filepath)
    
    def test_full_pipeline(self, sample_data):
        """Test complete pipeline execution."""
        script = f"""
            load {sample_data}
            clean missing
            split 80/20 --target target
            train random_forest
            evaluate
        """
        
        result = run(script)
        
        assert result.success
        assert result.context.model is not None
        assert 'accuracy' in result.context.metrics
    
    def test_pipeline_api(self, sample_data):
        """Test Pipeline API."""
        pipeline = (Pipeline()
            .load(sample_data)
            .clean_missing()
            .split(0.8, target="target")
            .train("random_forest")
            .evaluate()
        )
        
        result = pipeline.run()
        
        assert result.success
        assert result.context.model is not None


class TestVisualization:
    """Test visualization functionality."""
    
    def test_ascii_visualization(self):
        """Test ASCII visualization."""
        from pipelinescript.visualizer import PipelineVisualizer
        
        parser = PipelineParser()
        ast = parser.parse("load data.csv\ntrain xgboost")
        
        visualizer = PipelineVisualizer()
        visualizer.ascii_art = True
        
        # Should not raise exception
        visualizer.visualize_pipeline(ast)


class TestErrorHandling:
    """Test error handling."""
    
    def test_invalid_command(self):
        """Test invalid command handling."""
        parser = PipelineParser()
        ast = parser.parse("invalid_command")
        
        compiler = PipelineCompiler()
        
        with pytest.raises(ValueError):
            compiler.compile(ast)
    
    def test_missing_file(self):
        """Test missing file handling."""
        script = "load nonexistent.csv"
        
        result = run(script)
        
        assert not result.success
        assert result.error is not None


def test_imports():
    """Test all imports work."""
    from pipelinescript import (
        Pipeline,
        PipelineParser,
        PipelineCompiler,
        PipelineExecutor,
        PipelineDebugger,
        PipelineVisualizer,
        run,
        parse,
        compile,
        debug
    )
    
    assert Pipeline is not None
    assert run is not None


def test_version():
    """Test version is accessible."""
    from pipelinescript import __version__
    
    assert __version__ == "0.1.0"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
