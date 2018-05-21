package com.proiect.pbr.repository;

import com.proiect.pbr.model.Fact;
import org.springframework.data.repository.PagingAndSortingRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface FactRepository extends PagingAndSortingRepository<Fact,Long>{
}
