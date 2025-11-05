"""
Performance and load tests for the SlotSwapper API.
"""
import pytest
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

from tests.factories import PerformanceDataGenerator, UserFactory, EventFactory


@pytest.mark.slow
class TestDatabasePerformance:
    """Test database query performance."""
    
    def test_user_query_performance(self, db_session):
        """Test performance of user queries with large dataset."""
        generator = PerformanceDataGenerator(db_session)
        
        # Create large user base
        start_time = time.time()
        users = generator.create_large_user_base(count=1000)
        creation_time = time.time() - start_time
        
        print(f"Created 1000 users in {creation_time:.2f} seconds")
        
        # Test query performance
        start_time = time.time()
        queried_users = db_session.query(User).limit(100).all()
        query_time = time.time() - start_time
        
        print(f"Queried 100 users in {query_time:.4f} seconds")
        
        assert len(queried_users) == 100
        assert query_time < 1.0  # Should complete within 1 second
    
    def test_event_query_performance(self, db_session):
        """Test performance of event queries."""
        generator = PerformanceDataGenerator(db_session)
        
        # Create users and events
        users = generator.create_large_user_base(count=100)
        events = generator.create_many_events(users, events_per_user=50)
        
        print(f"Created {len(events)} events")
        
        # Test various query patterns
        queries = [
            ("All events", lambda: db_session.query(Event).all()),
            ("Events by owner", lambda: db_session.query(Event).filter(Event.owner_id == users[0].id).all()),
            ("Swappable events", lambda: db_session.query(Event).filter(Event.status == "SWAPPABLE").all()),
            ("Future events", lambda: db_session.query(Event).filter(Event.start_time > datetime.utcnow()).all()),
        ]
        
        for query_name, query_func in queries:
            start_time = time.time()
            results = query_func()
            query_time = time.time() - start_time
            
            print(f"{query_name}: {len(results)} results in {query_time:.4f} seconds")
            assert query_time < 2.0  # Should complete within 2 seconds
    
    def test_swap_request_query_performance(self, db_session):
        """Test performance of swap request queries."""
        generator = PerformanceDataGenerator(db_session)
        
        # Create test data
        users = generator.create_large_user_base(count=50)
        events = generator.create_many_events(users, events_per_user=20)
        swap_requests = generator.create_many_swap_requests(events, request_count=1000)
        
        print(f"Created {len(swap_requests)} swap requests")
        
        # Test query performance
        test_user = users[0]
        
        queries = [
            ("Incoming requests", lambda: db_session.query(SwapRequest).join(Event, SwapRequest.requested_event_id == Event.id).filter(Event.owner_id == test_user.id).all()),
            ("Outgoing requests", lambda: db_session.query(SwapRequest).filter(SwapRequest.requester_id == test_user.id).all()),
            ("Pending requests", lambda: db_session.query(SwapRequest).filter(SwapRequest.status == "PENDING").all()),
        ]
        
        for query_name, query_func in queries:
            start_time = time.time()
            results = query_func()
            query_time = time.time() - start_time
            
            print(f"{query_name}: {len(results)} results in {query_time:.4f} seconds")
            assert query_time < 1.0  # Should complete within 1 second


@pytest.mark.slow
class TestAPIPerformance:
    """Test API endpoint performance."""
    
    def test_authentication_performance(self, client):
        """Test authentication endpoint performance."""
        # Create test user
        user_data = {
            "email": "perf@example.com",
            "name": "Performance User",
            "password": "perfpassword123"
        }
        
        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        
        login_data = {
            "email": user_data["email"],
            "password": user_data["password"]
        }
        
        # Test login performance
        login_times = []
        for _ in range(10):
            start_time = time.time()
            response = client.post("/auth/login", json=login_data)
            login_time = time.time() - start_time
            
            assert response.status_code == 200
            login_times.append(login_time)
        
        avg_login_time = statistics.mean(login_times)
        max_login_time = max(login_times)
        
        print(f"Average login time: {avg_login_time:.4f}s, Max: {max_login_time:.4f}s")
        
        assert avg_login_time < 0.5  # Average should be under 500ms
        assert max_login_time < 1.0  # Max should be under 1s
    
    def test_event_creation_performance(self, client, auth_headers):
        """Test event creation performance."""
        creation_times = []
        
        for i in range(20):
            event_data = {
                "title": f"Performance Test Event {i}",
                "start_time": (datetime.utcnow() + timedelta(hours=i+1)).isoformat(),
                "end_time": (datetime.utcnow() + timedelta(hours=i+2)).isoformat()
            }
            
            start_time = time.time()
            response = client.post("/events/", json=event_data, headers=auth_headers)
            creation_time = time.time() - start_time
            
            assert response.status_code == 201
            creation_times.append(creation_time)
        
        avg_creation_time = statistics.mean(creation_times)
        max_creation_time = max(creation_times)
        
        print(f"Average event creation time: {avg_creation_time:.4f}s, Max: {max_creation_time:.4f}s")
        
        assert avg_creation_time < 0.3  # Average should be under 300ms
        assert max_creation_time < 1.0  # Max should be under 1s
    
    def test_event_listing_performance(self, client, auth_headers):
        """Test event listing performance with many events."""
        # Create many events first
        for i in range(100):
            event_data = {
                "title": f"List Test Event {i}",
                "start_time": (datetime.utcnow() + timedelta(hours=i+1)).isoformat(),
                "end_time": (datetime.utcnow() + timedelta(hours=i+2)).isoformat()
            }
            client.post("/events/", json=event_data, headers=auth_headers)
        
        # Test listing performance
        list_times = []
        for _ in range(10):
            start_time = time.time()
            response = client.get("/events/", headers=auth_headers)
            list_time = time.time() - start_time
            
            assert response.status_code == 200
            list_times.append(list_time)
        
        avg_list_time = statistics.mean(list_times)
        max_list_time = max(list_times)
        
        print(f"Average event listing time: {avg_list_time:.4f}s, Max: {max_list_time:.4f}s")
        
        assert avg_list_time < 0.5  # Average should be under 500ms
        assert max_list_time < 1.0  # Max should be under 1s


@pytest.mark.slow
class TestConcurrentAccess:
    """Test concurrent access scenarios."""
    
    def test_concurrent_user_registration(self, client):
        """Test concurrent user registrations."""
        def register_user(user_id):
            user_data = {
                "email": f"concurrent{user_id}@example.com",
                "name": f"Concurrent User {user_id}",
                "password": "concurrentpassword123"
            }
            
            start_time = time.time()
            response = client.post("/auth/register", json=user_data)
            end_time = time.time()
            
            return {
                "user_id": user_id,
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "success": response.status_code == 201
            }
        
        # Test with 20 concurrent registrations
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(register_user, i) for i in range(20)]
            results = [future.result() for future in as_completed(futures)]
        
        # Analyze results
        successful_registrations = [r for r in results if r["success"]]
        failed_registrations = [r for r in results if not r["success"]]
        
        response_times = [r["response_time"] for r in successful_registrations]
        avg_response_time = statistics.mean(response_times) if response_times else 0
        
        print(f"Successful registrations: {len(successful_registrations)}/20")
        print(f"Average response time: {avg_response_time:.4f}s")
        
        assert len(successful_registrations) == 20  # All should succeed
        assert avg_response_time < 2.0  # Should be reasonably fast
    
    def test_concurrent_event_creation(self, client, auth_headers):
        """Test concurrent event creation by same user."""
        def create_event(event_id):
            event_data = {
                "title": f"Concurrent Event {event_id}",
                "start_time": (datetime.utcnow() + timedelta(hours=event_id+1)).isoformat(),
                "end_time": (datetime.utcnow() + timedelta(hours=event_id+2)).isoformat()
            }
            
            start_time = time.time()
            response = client.post("/events/", json=event_data, headers=auth_headers)
            end_time = time.time()
            
            return {
                "event_id": event_id,
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "success": response.status_code == 201
            }
        
        # Test with 15 concurrent event creations
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(create_event, i) for i in range(15)]
            results = [future.result() for future in as_completed(futures)]
        
        successful_creations = [r for r in results if r["success"]]
        response_times = [r["response_time"] for r in successful_creations]
        avg_response_time = statistics.mean(response_times) if response_times else 0
        
        print(f"Successful event creations: {len(successful_creations)}/15")
        print(f"Average response time: {avg_response_time:.4f}s")
        
        assert len(successful_creations) == 15  # All should succeed
        assert avg_response_time < 1.0  # Should be reasonably fast
    
    def test_concurrent_swap_requests(self, client, db_session):
        """Test concurrent swap request creation and responses."""
        # Setup: Create users and events
        from tests.factories import TestDataBuilder
        
        builder = TestDataBuilder(db_session)
        scenario = builder.create_swap_scenario()
        
        user1 = scenario['user1']
        user2 = scenario['user2']
        event1 = scenario['swappable_event1']
        event2 = scenario['swappable_event2']
        
        # Create auth tokens
        from auth import create_access_token
        
        token1 = create_access_token(data={"sub": str(user1.id)})
        token2 = create_access_token(data={"sub": str(user2.id)})
        
        headers1 = {"Authorization": f"Bearer {token1}"}
        headers2 = {"Authorization": f"Bearer {token2}"}
        
        def create_swap_request(request_id):
            swap_data = {
                "offered_event_id": event1.id,
                "requested_event_id": event2.id
            }
            
            start_time = time.time()
            response = client.post("/swaps/request", json=swap_data, headers=headers1)
            end_time = time.time()
            
            return {
                "request_id": request_id,
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "success": response.status_code in [201, 400]  # 400 for duplicate is expected
            }
        
        # Test with multiple concurrent swap requests (should mostly fail due to duplicates)
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = [executor.submit(create_swap_request, i) for i in range(5)]
            results = [future.result() for future in as_completed(futures)]
        
        successful_requests = [r for r in results if r["status_code"] == 201]
        duplicate_requests = [r for r in results if r["status_code"] == 400]
        
        print(f"Successful swap requests: {len(successful_requests)}")
        print(f"Duplicate requests (expected): {len(duplicate_requests)}")
        
        # Only one should succeed, others should be duplicates
        assert len(successful_requests) == 1
        assert len(duplicate_requests) >= 1


@pytest.mark.slow
class TestMemoryUsage:
    """Test memory usage patterns."""
    
    def test_large_dataset_memory_usage(self, db_session):
        """Test memory usage with large datasets."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        generator = PerformanceDataGenerator(db_session)
        
        # Create large dataset
        users = generator.create_large_user_base(count=500)
        events = generator.create_many_events(users, events_per_user=10)
        
        mid_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create swap requests
        swap_requests = generator.create_many_swap_requests(events, request_count=1000)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        print(f"Initial memory: {initial_memory:.2f} MB")
        print(f"After users/events: {mid_memory:.2f} MB")
        print(f"Final memory: {final_memory:.2f} MB")
        print(f"Total increase: {final_memory - initial_memory:.2f} MB")
        
        # Memory increase should be reasonable
        memory_increase = final_memory - initial_memory
        assert memory_increase < 500  # Should not increase by more than 500MB
    
    def test_api_memory_leak(self, client, auth_headers):
        """Test for memory leaks in API endpoints."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Make many API calls
        for i in range(100):
            # Create event
            event_data = {
                "title": f"Memory Test Event {i}",
                "start_time": (datetime.utcnow() + timedelta(hours=i+1)).isoformat(),
                "end_time": (datetime.utcnow() + timedelta(hours=i+2)).isoformat()
            }
            client.post("/events/", json=event_data, headers=auth_headers)
            
            # List events
            client.get("/events/", headers=auth_headers)
            
            # Get user info
            client.get("/auth/me", headers=auth_headers)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        print(f"Memory increase after 300 API calls: {memory_increase:.2f} MB")
        
        # Memory increase should be minimal for API calls
        assert memory_increase < 50  # Should not increase by more than 50MB


# Utility functions for performance testing

def measure_execution_time(func, *args, **kwargs):
    """Measure execution time of a function."""
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    
    return result, end_time - start_time


def run_performance_benchmark(client, endpoint, method="GET", data=None, headers=None, iterations=10):
    """Run a performance benchmark on an API endpoint."""
    times = []
    
    for _ in range(iterations):
        start_time = time.time()
        
        if method.upper() == "GET":
            response = client.get(endpoint, headers=headers)
        elif method.upper() == "POST":
            response = client.post(endpoint, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = client.put(endpoint, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = client.delete(endpoint, headers=headers)
        
        end_time = time.time()
        times.append(end_time - start_time)
    
    return {
        "avg_time": statistics.mean(times),
        "min_time": min(times),
        "max_time": max(times),
        "median_time": statistics.median(times),
        "std_dev": statistics.stdev(times) if len(times) > 1 else 0
    }
