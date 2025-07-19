from netsuitesdk.internal.utils import PaginatedSearch

def get_transaction_data(ns_connection, transaction_type):
    """
    Get transaction data for types not in SEARCH_RECORD_TYPES
    
    Args:
        ns_connection: NetSuite connection object
        transaction_type: String like 'Invoice', 'VendorCredit', 'CreditMemo'
    
    Returns:
        List of transaction records
    """
    try:
        # Create search field for transaction type
        search_field = ns_connection.client.SearchStringField(
            searchValue=transaction_type, 
            operator='is'
        )
        
        # Create basic search
        basic_search = ns_connection.client.basic_search_factory(
            'Transaction', 
            recordType=search_field
        )
        
        # Create paginated search
        ps = PaginatedSearch(
            client=ns_connection.client, 
            type_name='Transaction', 
            basic_search=basic_search,
            pageSize=100
        )
        
        # Get all records
        records = []
        if ps.num_records > 0:
            for page in range(1, ps.total_pages + 1):
                ps.goto_page(page)
                if ps.records:
                    records.extend(ps.records)
        
        return records
        
    except Exception as e:
        print(f"Error getting {transaction_type} data: {e}")
        return []

def get_invoices(ns_connection):
    """Get all invoices"""
    return get_transaction_data(ns_connection, 'Invoice')

def get_vendor_credits(ns_connection):
    """Get all vendor credits"""
    return get_transaction_data(ns_connection, 'VendorCredit')

def get_credit_memos(ns_connection):
    """Get all credit memos"""
    return get_transaction_data(ns_connection, 'CreditMemo')

def get_custom_lists(ns_connection):
    """Get all custom lists using search operation"""
    try:
        from netsuitesdk.internal.utils import PaginatedSearch
        
        # Create basic search for custom lists
        basic_search = ns_connection.client.basic_search_factory('CustomList')
        
        # Create paginated search
        ps = PaginatedSearch(
            client=ns_connection.client, 
            type_name='CustomList', 
            basic_search=basic_search,
            pageSize=100
        )
        
        # Get all records
        records = []
        if ps.num_records > 0:
            for page in range(1, ps.total_pages + 1):
                ps.goto_page(page)
                if ps.records:
                    records.extend(ps.records)
        
        return records
        
    except Exception as e:
        print(f"Error getting custom lists: {e}")
        return []

def get_journal_entries(ns_connection):
    """Get all journal entries using a different approach to avoid memorized transaction error"""
    try:
        from netsuitesdk.internal.utils import PaginatedSearch
        
        # Create a search that excludes memorized transactions
        # Try to create a basic search with specific filters
        try:
            # Approach 1: Search for non-memorized journal entries
            is_memorized_field = ns_connection.client.SearchBooleanField(searchValue=False)
            basic_search = ns_connection.client.basic_search_factory(
                'Transaction',
                isMemorized=is_memorized_field
            )
            
            # Add record type filter for journal entries
            record_type_field = ns_connection.client.SearchStringField(searchValue='JournalEntry', operator='is')
            basic_search.recordType = record_type_field
            
            ps = PaginatedSearch(
                client=ns_connection.client,
                type_name='Transaction',
                basic_search=basic_search,
                pageSize=100
            )
            
            records = []
            if ps.num_records > 0:
                for page in range(1, ps.total_pages + 1):
                    ps.goto_page(page)
                    if ps.records:
                        records.extend(ps.records)
            
            if records:
                print(f"Successfully got {len(records)} journal entries (non-memorized)")
                return records
                
        except Exception as e:
            print(f"Approach 1 failed: {e}")
        
        # Approach 2: Try direct search without memorized filter
        try:
            ps = PaginatedSearch(
                client=ns_connection.client,
                type_name='Transaction',
                pageSize=100
            )
            
            records = []
            if ps.num_records > 0:
                for page in range(1, ps.total_pages + 1):
                    ps.goto_page(page)
                    if ps.records:
                        # Filter for journal entries manually
                        journal_records = [r for r in ps.records if hasattr(r, 'recordType') and r.recordType == 'JournalEntry']
                        records.extend(journal_records)
            
            if records:
                print(f"Successfully got {len(records)} journal entries (filtered)")
                return records
                
        except Exception as e:
            print(f"Approach 2 failed: {e}")
        
        print("All approaches failed for journal entries")
        return []
        
    except Exception as e:
        print(f"Error getting journal entries: {e}")
        return []

def get_custom_records(ns_connection, rec_type_id):
    """Get custom records by type ID"""
    try:
        from netsuitesdk.internal.utils import PaginatedSearch
        
        # Create custom record type reference
        custom_record_type = ns_connection.client.CustomRecordType(internalId=rec_type_id)
        
        # Create search basic
        search_basic = ns_connection.client.CustomRecordSearchBasic(recType=custom_record_type)
        
        # Create paginated search
        ps = PaginatedSearch(
            client=ns_connection.client, 
            type_name='CustomRecord', 
            basic_search=search_basic,
            pageSize=100
        )
        
        # Get all records
        records = []
        if ps.num_records > 0:
            for page in range(1, ps.total_pages + 1):
                ps.goto_page(page)
                if ps.records:
                    records.extend(ps.records)
        
        return records
        
    except Exception as e:
        print(f"Error getting custom records: {e}")
        return []

def get_custom_segments(ns_connection):
    """Get all custom segments using the correct search approach"""
    try:
        from netsuitesdk.internal.utils import PaginatedSearch
        
        # Since CustomSegmentSearch doesn't exist, try using the base search
        # Custom segments might be accessible through a different approach
        
        # Approach 1: Try direct search without specific search class
        try:
            ps = PaginatedSearch(
                client=ns_connection.client, 
                type_name='CustomSegment', 
                pageSize=100
            )
            
            records = []
            if ps.num_records > 0:
                for page in range(1, ps.total_pages + 1):
                    ps.goto_page(page)
                    if ps.records:
                        records.extend(ps.records)
            
            if records:
                print(f"Successfully got {len(records)} custom segments")
                return records
                
        except Exception as e:
            print(f"Direct search failed: {e}")
        
        # Approach 2: Try using getAll if it's in GET_ALL_RECORD_TYPES
        try:
            from netsuitesdk.internal.constants import GET_ALL_RECORD_TYPES
            if 'customSegment' in GET_ALL_RECORD_TYPES:
                records = ns_connection.client.getAll(recordType='CustomSegment')
                if records:
                    print(f"Successfully got {len(records)} custom segments via getAll")
                    return records
        except Exception as e:
            print(f"getAll approach failed: {e}")
        
        # Approach 3: Try to find custom segments through a different entity
        # Sometimes custom segments are accessible through other means
        try:
            # Try searching for custom segments through custom lists
            custom_lists = get_custom_lists(ns_connection)
            if custom_lists:
                print(f"Found {len(custom_lists)} custom lists, but no direct custom segments")
                return []
        except Exception as e:
            print(f"Custom lists approach failed: {e}")
        
        print("All approaches failed for custom segments")
        return []
        
    except Exception as e:
        print(f"Error getting custom segments: {e}")
        return []

def discover_custom_record_types(ns_connection):
    """Discover available custom record types"""
    try:
        # Try to get all custom record types using a broad search
        from netsuitesdk.internal.utils import PaginatedSearch
        
        # Create a basic search without specific filters
        basic_search = ns_connection.client.basic_search_factory('CustomRecordType')
        
        # Create paginated search
        ps = PaginatedSearch(
            client=ns_connection.client, 
            type_name='CustomRecordType', 
            basic_search=basic_search,
            pageSize=100
        )
        
        # Get all records
        records = []
        if ps.num_records > 0:
            for page in range(1, ps.total_pages + 1):
                ps.goto_page(page)
                if ps.records:
                    records.extend(ps.records)
        
        return records
        
    except Exception as e:
        print(f"Error discovering custom record types: {e}")
        return []

def get_custom_record_types_by_name(ns_connection, type_name):
    """Get custom record types by name"""
    try:
        from netsuitesdk.internal.utils import PaginatedSearch
        
        # Create search field for type name
        search_field = ns_connection.client.SearchStringField(
            searchValue=type_name, 
            operator='contains'
        )
        
        # Create basic search
        basic_search = ns_connection.client.basic_search_factory(
            'CustomRecordType', 
            name=search_field
        )
        
        # Create paginated search
        ps = PaginatedSearch(
            client=ns_connection.client, 
            type_name='CustomRecordType', 
            basic_search=basic_search,
            pageSize=100
        )
        
        # Get all records
        records = []
        if ps.num_records > 0:
            for page in range(1, ps.total_pages + 1):
                ps.goto_page(page)
                if ps.records:
                    records.extend(ps.records)
        
        return records
        
    except Exception as e:
        print(f"Error getting custom record types by name: {e}")
        return []

def get_usages(ns_connection):
    """Get all usages using the correct approach"""
    try:
        # Since UsageSearch doesn't exist, try different approaches
        
        # Approach 1: Try direct search without specific search class
        try:
            from netsuitesdk.internal.utils import PaginatedSearch
            
            ps = PaginatedSearch(
                client=ns_connection.client, 
                type_name='Usage', 
                pageSize=100
            )
            
            records = []
            if ps.num_records > 0:
                for page in range(1, ps.total_pages + 1):
                    ps.goto_page(page)
                    if ps.records:
                        records.extend(ps.records)
            
            if records:
                print(f"Successfully got {len(records)} usages via direct search")
                return records
                
        except Exception as e:
            print(f"Direct search failed: {e}")
        
        # Approach 2: Try using getAll if it's in GET_ALL_RECORD_TYPES
        try:
            from netsuitesdk.internal.constants import GET_ALL_RECORD_TYPES
            if 'usage' in GET_ALL_RECORD_TYPES:
                records = ns_connection.client.getAll(recordType='Usage')
                if records:
                    print(f"Successfully got {len(records)} usages via getAll")
                    return records
        except Exception as e:
            print(f"getAll approach failed: {e}")
        
        # Approach 3: Try transaction search for usage records
        try:
            records = get_transaction_data(ns_connection, 'Usage')
            if records:
                print(f"Successfully got {len(records)} usages via transaction search")
                return records
        except Exception as e:
            print(f"Transaction search failed: {e}")
        
        # Approach 4: Try to create usage records manually and search
        try:
            # Try to create a basic search manually
            from netsuitesdk.internal.utils import PaginatedSearch
            
            # Create a basic search without specific search class
            basic_search = ns_connection.client.basic_search_factory('Usage')
            
            ps = PaginatedSearch(
                client=ns_connection.client, 
                type_name='Usage', 
                basic_search=basic_search,
                pageSize=100
            )
            
            records = []
            if ps.num_records > 0:
                for page in range(1, ps.total_pages + 1):
                    ps.goto_page(page)
                    if ps.records:
                        records.extend(ps.records)
            
            if records:
                print(f"Successfully got {len(records)} usages via basic search")
                return records
                
        except Exception as e:
            print(f"Basic search failed: {e}")
        
        print("All approaches failed for usages")
        return []
        
    except Exception as e:
        print(f"Error getting usages: {e}")
        return []

def diagnose_available_types(ns_connection):
    """Diagnose what types are available in the NetSuite client"""
    try:
        print("=== Available Search Types ===")
        from netsuitesdk.internal.constants import SEARCH_RECORD_TYPES
        for i, search_type in enumerate(SEARCH_RECORD_TYPES, 1):
            print(f"{i:3d}. {search_type}")
        
        print("\n=== Available Complex Types (partial) ===")
        complex_types = list(ns_connection.client._complex_types.keys())
        # Filter for relevant types
        relevant_types = [t for t in complex_types if any(x in t.lower() for x in ['journal', 'segment', 'list', 'usage', 'custom'])]
        for i, complex_type in enumerate(relevant_types, 1):
            print(f"{i:3d}. {complex_type}")
        
        print("\n=== Testing Specific Types ===")
        test_types = ['JournalEntry', 'journalEntry', 'CustomSegment', 'CustomList', 'Usage']
        for test_type in test_types:
            try:
                # Try to get the complex type
                complex_type = ns_connection.client.get_complex_type(test_type)
                print(f"✓ {test_type} - Available")
            except:
                print(f"✗ {test_type} - Not available")
                
    except Exception as e:
        print(f"Error in diagnosis: {e}")