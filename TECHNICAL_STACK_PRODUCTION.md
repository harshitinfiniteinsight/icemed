# Technical Stack Recommendation - Production Grade ICE Reconciliation System

**Document Version:** 1.0  
**Date:** December 10, 2025  
**Prepared For:** PRM Healthcare Billing  
**Project:** ICE Charge Import & Reconciliation Automation

---

## Executive Summary

This document presents three technical stack options for production deployment of the ICE Reconciliation System, with detailed justification, comparison, and recommendations. Each option is evaluated based on performance, scalability, security, maintainability, and cost-effectiveness for a healthcare billing application handling PHI.

**Recommended Stack:** Option 1 - Python FastAPI + PostgreSQL (Best balance of performance, development speed, and healthcare ecosystem compatibility)

---

## Table of Contents

1. [Requirements Analysis](#1-requirements-analysis)
2. [Stack Option 1: Python FastAPI + PostgreSQL](#2-stack-option-1-python-fastapi--postgresql)
3. [Stack Option 2: Node.js + TypeScript + PostgreSQL](#3-stack-option-2-nodejs--typescript--postgresql)
4. [Stack Option 2: Java Spring Boot + PostgreSQL](#4-stack-option-3-java-spring-boot--postgresql)
5. [Comparison Matrix](#5-comparison-matrix)
6. [Recommendation](#6-recommendation)
7. [Migration Path](#7-migration-path)

---

## 1. Requirements Analysis

### 1.1 Functional Requirements
- Process Excel files (ICE exports)
- Integrate with EBS (Electronic Billing System)
- Generate reconciliation Excel files
- Maintain Master Missing historical ledger
- Handle 1000+ encounters per file
- Support scheduled/automated processing
- Deliver files to ICE automatically

### 1.2 Non-Functional Requirements
- **Performance:** Process 5000+ rows in < 5 minutes
- **Security:** HIPAA compliance, PHI protection, encryption
- **Reliability:** 99.9% uptime, error recovery
- **Scalability:** Handle multiple concurrent file processing
- **Maintainability:** Easy to update, debug, extend
- **Integration:** Connect to existing PRM tools and EBS

### 1.3 Technical Constraints
- Must integrate with existing PRM charge import tool (Python-based)
- EBS API likely REST/SOAP
- Excel file processing required
- Healthcare data (PHI) handling
- Compliance requirements (HIPAA, SOC 2)

---

## 2. Stack Option 1: Python FastAPI + PostgreSQL

### 2.1 Technology Components

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Backend Framework** | FastAPI | 0.104+ | High-performance async API |
| **Language** | Python | 3.11+ | Core logic, Excel processing |
| **Database** | PostgreSQL | 15+ | Master Missing, audit logs |
| **ORM** | SQLAlchemy | 2.0+ | Database abstraction |
| **Migrations** | Alembic | 1.12+ | Schema versioning |
| **Task Queue** | Celery | 5.3+ | Async file processing |
| **Message Broker** | Redis/RabbitMQ | Latest | Task queue backend |
| **File Storage** | AWS S3 / Azure Blob | Latest | Output file storage |
| **Cache** | Redis | 7.2+ | Session, result caching |
| **Authentication** | FastAPI-Users + JWT | Latest | User auth, API security |
| **Monitoring** | Prometheus + Grafana | Latest | Metrics, dashboards |
| **Logging** | ELK Stack (Elasticsearch) | Latest | Centralized logging |
| **Excel Processing** | openpyxl | 3.1+ | Excel read/write |
| **API Client** | httpx | 0.25+ | EBS API calls |
| **Validation** | Pydantic | 2.5+ | Data validation |
| **Testing** | pytest | 7.4+ | Unit/integration tests |

### 2.2 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer (ALB)                  │
│                  SSL Termination, WAF                  │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌────────▼────────┐
│  FastAPI API   │            │  FastAPI API   │
│   (Instance 1) │            │  (Instance 2)  │
└───────┬────────┘            └────────┬────────┘
        │                            │
        └───────────────┬────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌────────▼────────┐
│   Celery       │            │   Celery        │
│   Workers      │            │   Workers       │
└───────┬────────┘            └────────┬────────┘
        │                            │
        └───────────────┬────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌────────▼────────┐
│  PostgreSQL    │            │     Redis      │
│  (Primary +    │            │   (Cache +     │
│   Replica)     │            │   Queue)       │
└────────────────┘            └────────────────┘
        │
┌───────▼────────┐
│   AWS S3 /     │
│   Azure Blob   │
│   (File Store) │
└────────────────┘
```

### 2.3 Justification

#### ✅ Advantages

1. **Seamless Integration**
   - Existing PRM tool is Python-based → Easy integration
   - Can import/reuse existing modules
   - Same language ecosystem

2. **Excel Processing Excellence**
   - Python has best Excel libraries (openpyxl, pandas)
   - Mature ecosystem for data processing
   - Easy to handle complex Excel operations

3. **FastAPI Performance**
   - Async/await support → High concurrency
   - Automatic API documentation (OpenAPI/Swagger)
   - Type hints + Pydantic → Type safety
   - Comparable to Node.js performance

4. **Healthcare Ecosystem**
   - Many healthcare APIs have Python SDKs
   - Common in healthcare data processing
   - Strong library support for HL7, FHIR

5. **Development Speed**
   - Rapid prototyping (current prototype proves this)
   - Rich ecosystem (libraries for everything)
   - Easy to find Python developers

6. **Database Flexibility**
   - SQLAlchemy supports multiple databases
   - Easy to switch if needed
   - Excellent ORM with migrations

#### ⚠️ Considerations

1. **GIL Limitations**
   - Python GIL limits true parallelism
   - Mitigated by: Celery workers (separate processes), async I/O

2. **Memory Usage**
   - Can be higher than compiled languages
   - Mitigated by: Proper resource management, caching

3. **Type Safety**
   - Dynamic typing (though FastAPI + Pydantic help)
   - Mitigated by: Type hints, mypy, Pydantic validation

### 2.4 Use Cases Best Suited For

- ✅ Healthcare data processing
- ✅ Excel-heavy workflows
- ✅ Integration with Python-based systems
- ✅ Rapid development requirements
- ✅ API-first architectures
- ✅ Async task processing

---

## 3. Stack Option 2: Node.js + TypeScript + PostgreSQL

### 3.1 Technology Components

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Backend Framework** | Express.js / NestJS | 4.18+ / 10+ | API framework |
| **Language** | TypeScript | 5.3+ | Type-safe JavaScript |
| **Database** | PostgreSQL | 15+ | Master Missing, audit logs |
| **ORM** | Prisma / TypeORM | Latest | Database abstraction |
| **Task Queue** | BullMQ | 5.0+ | Async job processing |
| **Message Broker** | Redis | 7.2+ | Task queue backend |
| **File Storage** | AWS S3 / Azure Blob | Latest | Output file storage |
| **Cache** | Redis | 7.2+ | Session, result caching |
| **Authentication** | Passport.js + JWT | Latest | User auth, API security |
| **Monitoring** | Prometheus + Grafana | Latest | Metrics, dashboards |
| **Logging** | Winston + ELK | Latest | Centralized logging |
| **Excel Processing** | ExcelJS | Latest | Excel read/write |
| **API Client** | Axios / Fetch | Latest | EBS API calls |
| **Validation** | Zod | 3.22+ | Schema validation |
| **Testing** | Jest / Vitest | Latest | Unit/integration tests |

### 3.2 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer (ALB)                  │
│                  SSL Termination, WAF                  │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌────────▼────────┐
│  Express/Nest  │            │  Express/Nest  │
│   (Instance 1) │            │  (Instance 2)  │
└───────┬────────┘            └────────┬────────┘
        │                            │
        └───────────────┬────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌────────▼────────┐
│   BullMQ       │            │   BullMQ        │
│   Workers      │            │   Workers       │
└───────┬────────┘            └────────┬────────┘
        │                            │
        └───────────────┬────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌────────▼────────┐
│  PostgreSQL    │            │     Redis      │
│  (Primary +    │            │   (Cache +     │
│   Replica)     │            │   Queue)       │
└────────────────┘            └────────────────┘
        │
┌───────▼────────┐
│   AWS S3 /     │
│   Azure Blob   │
│   (File Store) │
└────────────────┘
```

### 3.3 Justification

#### ✅ Advantages

1. **High Performance**
   - Event-driven, non-blocking I/O
   - Excellent for concurrent requests
   - Fast JSON processing

2. **TypeScript Type Safety**
   - Compile-time type checking
   - Better IDE support
   - Reduced runtime errors

3. **Unified Language**
   - Same language for frontend + backend
   - Code sharing possibilities
   - Easier for full-stack developers

4. **Rich Ecosystem**
   - npm has packages for everything
   - Active community
   - Fast iteration

5. **Microservices Ready**
   - Easy to break into services
   - Good containerization support
   - Cloud-native friendly

#### ⚠️ Considerations

1. **Excel Processing**
   - ExcelJS is good but less mature than Python libraries
   - May need more custom code for complex operations

2. **Integration Challenges**
   - Existing PRM tool is Python → Need API bridge
   - May require separate Python service for Excel processing

3. **TypeScript Learning Curve**
   - Team may need TypeScript training
   - More complex than plain JavaScript

4. **Callback Hell (if not using async/await)**
   - Can be mitigated with proper async patterns

### 3.4 Use Cases Best Suited For

- ✅ High-concurrency APIs
- ✅ Real-time applications
- ✅ Microservices architecture
- ✅ When frontend/backend share code
- ✅ JSON-heavy APIs
- ⚠️ Excel processing (less ideal)

---

## 4. Stack Option 3: Java Spring Boot + PostgreSQL

### 4.1 Technology Components

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Backend Framework** | Spring Boot | 3.2+ | Enterprise framework |
| **Language** | Java | 17+ (LTS) | Enterprise-grade language |
| **Database** | PostgreSQL | 15+ | Master Missing, audit logs |
| **ORM** | JPA/Hibernate | 6.4+ | Database abstraction |
| **Task Queue** | Spring Batch | 5.0+ | Batch processing |
| **Message Broker** | RabbitMQ / Kafka | Latest | Task queue backend |
| **File Storage** | AWS S3 / Azure Blob | Latest | Output file storage |
| **Cache** | Redis / Caffeine | Latest | Session, result caching |
| **Authentication** | Spring Security | 6.2+ | Enterprise security |
| **Monitoring** | Micrometer + Prometheus | Latest | Metrics, dashboards |
| **Logging** | Logback + ELK | Latest | Centralized logging |
| **Excel Processing** | Apache POI | 5.2+ | Excel read/write |
| **API Client** | WebClient / RestTemplate | Latest | EBS API calls |
| **Validation** | Bean Validation (JSR-303) | Latest | Data validation |
| **Testing** | JUnit 5 + Mockito | Latest | Unit/integration tests |

### 4.2 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Load Balancer (ALB)                  │
│                  SSL Termination, WAF                  │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌────────▼────────┐
│ Spring Boot    │            │ Spring Boot    │
│  (Instance 1)  │            │  (Instance 2)  │
└───────┬────────┘            └────────┬────────┘
        │                            │
        └───────────────┬────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌────────▼────────┐
│ Spring Batch   │            │ Spring Batch    │
│   Workers      │            │   Workers       │
└───────┬────────┘            └────────┬────────┘
        │                            │
        └───────────────┬────────────┘
                        │
        ┌───────────────┴───────────────┐
        │                               │
┌───────▼────────┐            ┌────────▼────────┐
│  PostgreSQL     │            │  RabbitMQ /     │
│  (Primary +     │            │   Kafka        │
│   Replica)     │            │   (Queue)      │
└────────────────┘            └────────────────┘
        │
┌───────▼────────┐
│   AWS S3 /     │
│   Azure Blob   │
│   (File Store) │
└────────────────┘
```

### 4.3 Justification

#### ✅ Advantages

1. **Enterprise-Grade**
   - Battle-tested in enterprise environments
   - Mature ecosystem
   - Strong security features (Spring Security)

2. **Performance & Scalability**
   - JVM optimization → Excellent performance
   - Handles high load well
   - Good for long-running processes

3. **Type Safety**
   - Strong static typing
   - Compile-time error detection
   - Better IDE support

4. **Spring Ecosystem**
   - Comprehensive framework (security, data, batch, etc.)
   - Less need for external libraries
   - Consistent patterns

5. **Long-Term Support**
   - Java LTS versions (17, 21)
   - Enterprise support available
   - Stable platform

6. **Excel Processing**
   - Apache POI is mature and powerful
   - Good for complex Excel operations

#### ⚠️ Considerations

1. **Development Speed**
   - More verbose than Python/Node.js
   - Slower iteration cycles
   - More boilerplate code

2. **Integration Challenges**
   - Existing PRM tool is Python → Need API bridge
   - Different language ecosystem

3. **Resource Usage**
   - Higher memory footprint
   - Slower startup times
   - More CPU intensive

4. **Learning Curve**
   - Spring framework complexity
   - Team may need training
   - Steeper learning curve

5. **Cost**
   - May require more infrastructure
   - Enterprise licenses (if using commercial tools)

### 4.4 Use Cases Best Suited For

- ✅ Enterprise environments
- ✅ High-throughput batch processing
- ✅ Complex business logic
- ✅ Long-term maintainability requirements
- ✅ When Java expertise exists
- ⚠️ Rapid development (less ideal)

---

## 5. Comparison Matrix

### 5.1 Detailed Comparison Table

| Criteria | Option 1: Python FastAPI | Option 2: Node.js/TypeScript | Option 3: Java Spring Boot |
|----------|-------------------------|------------------------------|---------------------------|
| **Performance** | ⭐⭐⭐⭐ (Excellent) | ⭐⭐⭐⭐⭐ (Outstanding) | ⭐⭐⭐⭐⭐ (Outstanding) |
| **Excel Processing** | ⭐⭐⭐⭐⭐ (Best libraries) | ⭐⭐⭐ (Good but less mature) | ⭐⭐⭐⭐ (Apache POI mature) |
| **Development Speed** | ⭐⭐⭐⭐⭐ (Very Fast) | ⭐⭐⭐⭐ (Fast) | ⭐⭐⭐ (Moderate) |
| **Integration with PRM Tool** | ⭐⭐⭐⭐⭐ (Same language) | ⭐⭐ (Different language) | ⭐⭐ (Different language) |
| **Type Safety** | ⭐⭐⭐⭐ (Pydantic helps) | ⭐⭐⭐⭐⭐ (TypeScript) | ⭐⭐⭐⭐⭐ (Java) |
| **Concurrency** | ⭐⭐⭐⭐ (Async/await) | ⭐⭐⭐⭐⭐ (Event-driven) | ⭐⭐⭐⭐ (Thread pool) |
| **Ecosystem Maturity** | ⭐⭐⭐⭐⭐ (Very mature) | ⭐⭐⭐⭐⭐ (Very mature) | ⭐⭐⭐⭐⭐ (Very mature) |
| **Healthcare Libraries** | ⭐⭐⭐⭐⭐ (Excellent) | ⭐⭐⭐ (Good) | ⭐⭐⭐⭐ (Good) |
| **Learning Curve** | ⭐⭐⭐⭐ (Easy) | ⭐⭐⭐ (Moderate) | ⭐⭐ (Steeper) |
| **Memory Usage** | ⭐⭐⭐ (Moderate) | ⭐⭐⭐⭐ (Low) | ⭐⭐ (Higher) |
| **Startup Time** | ⭐⭐⭐⭐ (Fast) | ⭐⭐⭐⭐⭐ (Very Fast) | ⭐⭐ (Slower) |
| **Error Handling** | ⭐⭐⭐⭐ (Good) | ⭐⭐⭐⭐ (Good) | ⭐⭐⭐⭐⭐ (Excellent) |
| **Testing Support** | ⭐⭐⭐⭐⭐ (pytest excellent) | ⭐⭐⭐⭐ (Jest/Vitest good) | ⭐⭐⭐⭐⭐ (JUnit excellent) |
| **Documentation** | ⭐⭐⭐⭐⭐ (Auto-generated) | ⭐⭐⭐⭐ (Good) | ⭐⭐⭐⭐ (Good) |
| **Community Support** | ⭐⭐⭐⭐⭐ (Very active) | ⭐⭐⭐⭐⭐ (Very active) | ⭐⭐⭐⭐ (Active) |
| **Cost (Infrastructure)** | ⭐⭐⭐⭐ (Moderate) | ⭐⭐⭐⭐⭐ (Lower) | ⭐⭐⭐ (Higher) |
| **HIPAA Compliance** | ⭐⭐⭐⭐ (Good support) | ⭐⭐⭐⭐ (Good support) | ⭐⭐⭐⭐⭐ (Enterprise-grade) |
| **Maintainability** | ⭐⭐⭐⭐ (Good) | ⭐⭐⭐⭐ (Good) | ⭐⭐⭐⭐⭐ (Excellent) |
| **Scalability** | ⭐⭐⭐⭐ (Good) | ⭐⭐⭐⭐⭐ (Excellent) | ⭐⭐⭐⭐⭐ (Excellent) |
| **Migration Effort** | ⭐⭐⭐⭐⭐ (Minimal - same language) | ⭐⭐ (Significant rewrite) | ⭐⭐ (Significant rewrite) |

### 5.2 Quantitative Comparison

| Metric | Option 1: FastAPI | Option 2: Node.js | Option 3: Spring Boot |
|--------|-------------------|-------------------|----------------------|
| **Lines of Code (Est.)** | ~8,000 | ~10,000 | ~12,000 |
| **Development Time** | 8-10 weeks | 10-12 weeks | 12-16 weeks |
| **Team Size Needed** | 2-3 developers | 2-3 developers | 3-4 developers |
| **Memory per Instance** | 512MB-1GB | 256MB-512MB | 1GB-2GB |
| **Request Latency (p50)** | 50-100ms | 30-80ms | 40-90ms |
| **Throughput (req/sec)** | 2,000-5,000 | 3,000-8,000 | 2,500-6,000 |
| **Excel Processing Time** | 2-3 min (5000 rows) | 3-4 min (5000 rows) | 2-3 min (5000 rows) |
| **Infrastructure Cost/Month** | $500-800 | $400-600 | $800-1,200 |

### 5.3 Feature-Specific Comparison

| Feature | Option 1: FastAPI | Option 2: Node.js | Option 3: Spring Boot |
|---------|------------------|-------------------|----------------------|
| **EBS API Integration** | ✅ Excellent (httpx) | ✅ Good (Axios) | ✅ Good (WebClient) |
| **Excel File Processing** | ✅✅✅ Best (openpyxl) | ✅ Good (ExcelJS) | ✅✅ Good (Apache POI) |
| **Database ORM** | ✅ Excellent (SQLAlchemy) | ✅ Good (Prisma/TypeORM) | ✅ Excellent (JPA) |
| **Task Queue** | ✅ Excellent (Celery) | ✅ Excellent (BullMQ) | ✅ Good (Spring Batch) |
| **Authentication** | ✅ Good (FastAPI-Users) | ✅ Good (Passport) | ✅✅✅ Excellent (Spring Security) |
| **API Documentation** | ✅✅✅ Auto (OpenAPI) | ✅ Good (Swagger) | ✅ Good (SpringDoc) |
| **Monitoring** | ✅ Good (Prometheus) | ✅ Good (Prometheus) | ✅ Excellent (Micrometer) |
| **Error Handling** | ✅ Good | ✅ Good | ✅✅✅ Excellent |
| **Validation** | ✅✅ Excellent (Pydantic) | ✅✅ Excellent (Zod) | ✅ Good (Bean Validation) |

---

## 6. Recommendation

### 6.1 Recommended Stack: Option 1 - Python FastAPI + PostgreSQL

**Rationale:**

1. **Seamless Integration** ⭐⭐⭐⭐⭐
   - Existing PRM tool is Python → Zero integration friction
   - Can reuse existing code/modules
   - Same development team expertise

2. **Excel Processing Excellence** ⭐⭐⭐⭐⭐
   - Best-in-class libraries (openpyxl, pandas)
   - Current prototype already proves this works
   - Mature ecosystem for data processing

3. **Development Speed** ⭐⭐⭐⭐⭐
   - FastAPI enables rapid development
   - Current prototype built quickly
   - Easy to iterate and extend

4. **Performance** ⭐⭐⭐⭐
   - FastAPI async/await → High concurrency
   - Celery for background processing
   - Sufficient for requirements (< 5 min for 5000 rows)

5. **Cost-Effectiveness** ⭐⭐⭐⭐
   - Lower infrastructure costs
   - Faster development → Lower dev costs
   - Open-source stack

6. **Migration Path** ⭐⭐⭐⭐⭐
   - Minimal migration effort
   - Can incrementally enhance current prototype
   - Low risk transition

### 6.2 When to Consider Alternatives

**Consider Option 2 (Node.js) if:**
- Frontend team wants to share code
- Need ultra-high concurrency (>10K req/sec)
- Excel processing is minimal

**Consider Option 3 (Java) if:**
- Enterprise mandates Java
- Need maximum type safety
- Long-term maintainability is top priority
- Have Java expertise in-house

---

## 7. Migration Path

### 7.1 From Prototype to Production (Option 1)

**Phase 1: Foundation (Weeks 1-2)**
- ✅ Set up PostgreSQL database
- ✅ Migrate Master Missing to database
- ✅ Implement SQLAlchemy models
- ✅ Set up Alembic migrations

**Phase 2: Core Enhancements (Weeks 3-4)**
- ✅ Replace in-memory storage with database
- ✅ Implement Celery for async processing
- ✅ Add Redis for caching/queue
- ✅ Set up AWS S3 for file storage

**Phase 3: EBS Integration (Weeks 5-6)**
- ✅ Replace Mock EBS with real EBS API client
- ✅ Implement retry logic, error handling
- ✅ Add EBS connection pooling
- ✅ Map EBS error codes to user messages

**Phase 4: Security (Weeks 7-8)**
- ✅ Implement FastAPI-Users authentication
- ✅ Add role-based access control
- ✅ Implement audit logging
- ✅ Add encryption for PHI data

**Phase 5: Automation (Weeks 9-10)**
- ✅ Set up scheduled jobs (Celery Beat)
- ✅ Implement email notifications
- ✅ Add SFTP file delivery
- ✅ Set up monitoring/alerting

**Phase 6: Testing & Deployment (Weeks 11-12)**
- ✅ Comprehensive test suite
- ✅ Performance testing
- ✅ Security audit
- ✅ Production deployment

### 7.2 Migration Effort Comparison

| Option | Migration Effort | Risk Level | Timeline |
|--------|-----------------|------------|----------|
| **Option 1: FastAPI** | Low (incremental) | Low | 8-10 weeks |
| **Option 2: Node.js** | High (rewrite) | Medium | 10-12 weeks |
| **Option 3: Spring Boot** | High (rewrite) | Medium-High | 12-16 weeks |

---

## 8. Infrastructure Recommendations

### 8.1 Recommended Architecture (Option 1)

**Application Layer:**
- **API Servers:** 2x EC2/ECS instances (t3.medium)
- **Workers:** 2x Celery workers (t3.large)
- **Load Balancer:** AWS ALB

**Data Layer:**
- **Database:** AWS RDS PostgreSQL (db.t3.medium, Multi-AZ)
- **Cache/Queue:** AWS ElastiCache Redis (cache.t3.medium)
- **File Storage:** AWS S3 (with lifecycle policies)

**Monitoring:**
- **Metrics:** CloudWatch + Prometheus
- **Logging:** CloudWatch Logs → ELK Stack
- **Alerting:** SNS + PagerDuty

**Security:**
- **WAF:** AWS WAF
- **Encryption:** KMS for encryption keys
- **Secrets:** AWS Secrets Manager

### 8.2 Estimated Monthly Costs

| Component | Option 1: FastAPI | Option 2: Node.js | Option 3: Spring Boot |
|-----------|------------------|-------------------|----------------------|
| **Compute (EC2/ECS)** | $200-300 | $150-250 | $300-500 |
| **Database (RDS)** | $150-200 | $150-200 | $200-300 |
| **Cache (Redis)** | $50-100 | $50-100 | $50-100 |
| **Storage (S3)** | $50-100 | $50-100 | $50-100 |
| **Monitoring** | $50-100 | $50-100 | $50-100 |
| **Total/Month** | **$500-800** | **$450-750** | **$650-1,100** |

---

## 9. Risk Assessment

### 9.1 Option 1: FastAPI - Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Python GIL limits | Medium | Low | Use Celery (separate processes), async I/O |
| Memory usage | Low | Medium | Proper resource management, caching |
| Type safety | Low | Low | Pydantic validation, type hints, mypy |
| Team expertise | Low | Low | Python is common, FastAPI is simple |

### 9.2 Option 2: Node.js - Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Excel processing | High | Medium | Use Python microservice for Excel if needed |
| PRM integration | High | High | API bridge, separate Python service |
| TypeScript learning | Medium | Medium | Training, gradual adoption |
| Callback complexity | Low | Low | Use async/await, proper patterns |

### 9.3 Option 3: Spring Boot - Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Development speed | Medium | High | Use Spring Boot starters, code generators |
| PRM integration | High | High | API bridge, separate Python service |
| Resource usage | Medium | Medium | Proper JVM tuning, resource limits |
| Learning curve | Medium | Medium | Training, pair programming |

---

## 10. Conclusion

### 10.1 Final Recommendation

**Recommended Stack: Option 1 - Python FastAPI + PostgreSQL**

**Key Reasons:**
1. ✅ **Best fit for current context** - Seamless integration with existing Python PRM tool
2. ✅ **Excel processing excellence** - Best libraries and proven in prototype
3. ✅ **Fastest time to market** - Can build on existing prototype
4. ✅ **Cost-effective** - Lower infrastructure and development costs
5. ✅ **Sufficient performance** - Meets all requirements (< 5 min for 5000 rows)
6. ✅ **Low risk** - Incremental migration from prototype

### 10.2 Decision Matrix Summary

| Factor | Weight | Option 1 | Option 2 | Option 3 |
|--------|--------|----------|----------|----------|
| **Integration Ease** | 25% | 5.0 | 2.0 | 2.0 |
| **Excel Processing** | 20% | 5.0 | 3.0 | 4.0 |
| **Development Speed** | 15% | 5.0 | 4.0 | 3.0 |
| **Performance** | 15% | 4.0 | 5.0 | 5.0 |
| **Cost** | 10% | 4.0 | 5.0 | 3.0 |
| **Maintainability** | 10% | 4.0 | 4.0 | 5.0 |
| **Security** | 5% | 4.0 | 4.0 | 5.0 |
| **Weighted Score** | | **4.55** | **3.65** | **3.50** |

**Winner: Option 1 (4.55/5.0)**

---

## 11. Next Steps

1. **Approve Stack Selection** - Review and approve Option 1
2. **Set Up Infrastructure** - Provision AWS/Azure resources
3. **Database Design** - Design PostgreSQL schema
4. **Begin Migration** - Start Phase 1 (Foundation)
5. **EBS Integration Planning** - Coordinate with EBS team
6. **Security Review** - HIPAA compliance planning

---

**Document Prepared By:** Technical Architecture Team  
**Review Required By:** CTO, Lead Developer, Security Team  
**Approval Required By:** Project Sponsor

---

**Last Updated:** December 10, 2025  
**Status:** Ready for Review
