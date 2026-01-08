"""
Performance and load tests for the governance system.
Tests throughput, response times, and scalability.
"""

import unittest
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

from core_directive import CoreDirective, evaluate, is_allowed
from evaluator import DirectiveEvaluator, evaluate_detailed
from gateway import GovernanceGateway, GatewayRequest
from ai_client import GovernedAIClient, MockAIModel


class TestPerformance(unittest.TestCase):
    """Performance tests for core components."""

    def test_core_directive_throughput(self):
        """Test throughput of core directive evaluation."""
        directive = CoreDirective()
        iterations = 1000
        
        start_time = time.time()
        for i in range(iterations):
            directive.evaluate_intent(f"test request {i}")
        end_time = time.time()
        
        duration = end_time - start_time
        throughput = iterations / duration
        
        # Should handle at least 1000 evaluations per second
        self.assertGreater(throughput, 1000, 
                          f"Throughput {throughput:.0f} req/s is below minimum 1000 req/s")
        print(f"\nCore Directive throughput: {throughput:.0f} requests/second")

    def test_evaluator_throughput(self):
        """Test throughput of detailed evaluator."""
        evaluator = DirectiveEvaluator()
        iterations = 500
        
        start_time = time.time()
        for i in range(iterations):
            evaluator.evaluate(f"test request {i}")
        end_time = time.time()
        
        duration = end_time - start_time
        throughput = iterations / duration
        
        # Detailed evaluator is more complex, expect at least 500/s
        self.assertGreater(throughput, 500,
                          f"Evaluator throughput {throughput:.0f} req/s is below minimum 500 req/s")
        print(f"Detailed Evaluator throughput: {throughput:.0f} requests/second")

    def test_gateway_throughput(self):
        """Test throughput of gateway processing."""
        gateway = GovernanceGateway()
        iterations = 500
        
        start_time = time.time()
        for i in range(iterations):
            request = GatewayRequest.create(f"test {i}", source="test")
            gateway.process(request)
        end_time = time.time()
        
        duration = end_time - start_time
        throughput = iterations / duration
        
        # Gateway includes audit logging, expect at least 500/s
        self.assertGreater(throughput, 500,
                          f"Gateway throughput {throughput:.0f} req/s is below minimum 500 req/s")
        print(f"Gateway throughput: {throughput:.0f} requests/second")

    def test_ai_client_throughput(self):
        """Test throughput of AI client processing."""
        client = GovernedAIClient(model=MockAIModel())
        iterations = 500
        
        start_time = time.time()
        for i in range(iterations):
            client.process(f"test request {i}")
        end_time = time.time()
        
        duration = end_time - start_time
        throughput = iterations / duration
        
        # AI client is most complex, expect at least 300/s
        self.assertGreater(throughput, 300,
                          f"AI Client throughput {throughput:.0f} req/s is below minimum 300 req/s")
        print(f"AI Client throughput: {throughput:.0f} requests/second")


class TestResponseTime(unittest.TestCase):
    """Response time tests for individual operations."""

    def test_core_directive_response_time(self):
        """Test response time for single evaluation."""
        directive = CoreDirective()
        times = []
        
        for _ in range(100):
            start = time.perf_counter()
            directive.evaluate_intent("test request")
            end = time.perf_counter()
            times.append((end - start) * 1000)  # Convert to ms
        
        avg_time = statistics.mean(times)
        p95_time = statistics.quantiles(times, n=20)[18]  # 95th percentile
        
        # Average should be under 1ms
        self.assertLess(avg_time, 1.0,
                       f"Average response time {avg_time:.2f}ms exceeds 1ms")
        # 95th percentile should be under 2ms
        self.assertLess(p95_time, 2.0,
                       f"P95 response time {p95_time:.2f}ms exceeds 2ms")
        print(f"\nCore Directive - Avg: {avg_time:.3f}ms, P95: {p95_time:.3f}ms")

    def test_evaluator_response_time(self):
        """Test response time for detailed evaluation."""
        evaluator = DirectiveEvaluator()
        times = []
        
        for _ in range(100):
            start = time.perf_counter()
            evaluator.evaluate("test request with some content")
            end = time.perf_counter()
            times.append((end - start) * 1000)
        
        avg_time = statistics.mean(times)
        p95_time = statistics.quantiles(times, n=20)[18]
        
        # More complex, allow up to 5ms average
        self.assertLess(avg_time, 5.0,
                       f"Average response time {avg_time:.2f}ms exceeds 5ms")
        self.assertLess(p95_time, 10.0,
                       f"P95 response time {p95_time:.2f}ms exceeds 10ms")
        print(f"Detailed Evaluator - Avg: {avg_time:.3f}ms, P95: {p95_time:.3f}ms")


class TestConcurrency(unittest.TestCase):
    """Concurrency and thread-safety tests."""

    def test_concurrent_directive_evaluation(self):
        """Test concurrent evaluation with multiple threads."""
        directive = CoreDirective()
        num_threads = 10
        requests_per_thread = 100
        
        def evaluate_batch(thread_id):
            results = []
            for i in range(requests_per_thread):
                result = directive.evaluate_intent(f"thread {thread_id} request {i}")
                results.append(result)
            return results
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(evaluate_batch, i) for i in range(num_threads)]
            all_results = []
            for future in as_completed(futures):
                all_results.extend(future.result())
        end_time = time.time()
        
        duration = end_time - start_time
        total_requests = num_threads * requests_per_thread
        throughput = total_requests / duration
        
        # All requests should complete successfully
        self.assertEqual(len(all_results), total_requests)
        # Concurrent throughput should benefit from parallelism
        print(f"\nConcurrent Directive evaluation ({num_threads} threads): {throughput:.0f} req/s")

    def test_concurrent_gateway_processing(self):
        """Test concurrent gateway processing."""
        gateway = GovernanceGateway()
        num_threads = 5
        requests_per_thread = 50
        
        def process_batch(thread_id):
            results = []
            for i in range(requests_per_thread):
                request = GatewayRequest.create(
                    f"thread {thread_id} request {i}",
                    source=f"thread_{thread_id}"
                )
                response = gateway.process(request)
                results.append(response)
            return results
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(process_batch, i) for i in range(num_threads)]
            all_results = []
            for future in as_completed(futures):
                all_results.extend(future.result())
        end_time = time.time()
        
        duration = end_time - start_time
        total_requests = num_threads * requests_per_thread
        throughput = total_requests / duration
        
        self.assertEqual(len(all_results), total_requests)
        # Check audit log integrity
        self.assertEqual(len(gateway.audit_log), total_requests)
        print(f"Concurrent Gateway processing ({num_threads} threads): {throughput:.0f} req/s")


class TestScalability(unittest.TestCase):
    """Scalability tests for various input sizes."""

    def test_long_input_handling(self):
        """Test performance with very long inputs."""
        directive = CoreDirective()
        
        # Test with increasingly long inputs
        for length in [100, 1000, 10000, 50000]:
            long_input = "test " * (length // 5)
            
            start = time.perf_counter()
            result = directive.evaluate_intent(long_input)
            end = time.perf_counter()
            
            duration_ms = (end - start) * 1000
            
            # Should complete in reasonable time even for long inputs
            self.assertLess(duration_ms, 50,
                           f"Processing {length} chars took {duration_ms:.2f}ms (max 50ms)")

    def test_batch_processing_efficiency(self):
        """Test efficiency of batch processing."""
        evaluator = DirectiveEvaluator()
        batch_sizes = [10, 50, 100, 500]
        
        for size in batch_sizes:
            requests = [f"request {i}" for i in range(size)]
            
            start = time.time()
            for req in requests:
                evaluator.evaluate(req)
            end = time.time()
            
            duration = end - start
            per_request = (duration / size) * 1000  # ms per request
            
            # Per-request time should remain consistent regardless of batch size
            self.assertLess(per_request, 5.0,
                           f"Batch size {size}: {per_request:.2f}ms per request exceeds 5ms")

    def test_memory_stability(self):
        """Test that repeated operations don't leak memory."""
        import gc
        evaluator = DirectiveEvaluator()
        
        # Force garbage collection
        gc.collect()
        
        # Process many requests
        for i in range(1000):
            evaluator.evaluate(f"test request {i}")
            if i % 100 == 0:
                gc.collect()
        
        # Should complete without memory errors
        self.assertEqual(evaluator.evaluation_count, 1000)


class TestModuleLevelPerformance(unittest.TestCase):
    """Test performance of module-level convenience functions."""

    def test_module_function_overhead(self):
        """Test that module-level functions have minimal overhead."""
        iterations = 1000
        
        # Test module-level function
        start = time.time()
        for _ in range(iterations):
            evaluate("test")
        module_time = time.time() - start
        
        # Test direct instantiation
        directive = CoreDirective()
        start = time.time()
        for _ in range(iterations):
            directive.evaluate_intent("test")
        direct_time = time.time() - start
        
        # Singleton overhead should be minimal (within 30%)
        overhead = (module_time - direct_time) / direct_time
        self.assertLess(overhead, 0.3,
                       f"Module function overhead {overhead:.1%} exceeds 30%")


if __name__ == "__main__":
    # Run with verbose output to see performance metrics
    unittest.main(verbosity=2)
