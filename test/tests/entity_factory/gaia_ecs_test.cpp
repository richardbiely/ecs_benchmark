#include "base.h"
#include "gaia-ecs/entities/EntityFactory.h"
#include "gaia-ecs/entities/HeroMonsterEntityFactory.h"
#include <catch2/catch_template_test_macros.hpp>
#include <catch2/catch_test_macros.hpp>

namespace ecs::benchmarks::gaia_ecs {

TEMPLATE_TEST_CASE_METHOD(ecs::benchmarks::EntityFactory_Fixture, "Test EntityFactory for gaia-ecs",
                          "[template][gaia][gaia-ecs][entity_factory]",
                          ecs::benchmarks::gaia_ecs::entities::EntityFactory) {
  GIVEN("EntityFactory") {
    ecs::benchmarks::EntityFactory_Fixture<TestType> entity_factory_fixture;
    // auto& entity_factory = entity_factory_fixture.m_entity_factory;
    ::gaia::ecs::World world;

    WHEN("create entity") {
      entity_factory_fixture.testCreateEntity(world);
    }
    WHEN("create minimal entity") {
      entity_factory_fixture.testCreateMinimalEntity(world);
    }
    WHEN("create single entity") {
      entity_factory_fixture.testCreateSingleEntity(world);
    }

    WHEN("destroy entity") {
      entity_factory_fixture.testDestroyEntity(world);
    }

    WHEN("get one component") {
      entity_factory_fixture.testGetComponentOne(world);
    }
  }
}

TEMPLATE_TEST_CASE_METHOD(ecs::benchmarks::HeroMonsterEntityFactory_Fixture,
                          "Test HeroMonsterEntityFactory for gaia-ecs",
                          "[template][gaia][gaia-ecs][entity_factory][hero][monster]",
                          ecs::benchmarks::gaia_ecs::entities::HeroMonsterEntityFactory) {
  GIVEN("HeroMonsterEntityFactory") {
    ecs::benchmarks::HeroMonsterEntityFactory_Fixture<TestType> entity_factory_fixture;
    // auto& entity_factory = entity_factory_fixture.m_entity_factory;
    ::gaia::ecs::World world;

    WHEN("create entity") {
      entity_factory_fixture.testCreateEntity(world);
    }

    WHEN("get one component") {
      entity_factory_fixture.testGetPlayerComponent(world);
    }
  }
}

} // namespace ecs::benchmarks::gaia_ecs