yaml_content = """
kwargs_common: &kwargs_common
  agent.search.max_debug_depth: 20 # debug down a branch for up to 20 steps
  agent.search.debug_prob: 1 # always debug when there's something to debug
  exec.timeout: 32400 # 9 hours limit _per step_, to match max of kaggle.com
  copy_data: False # use symbolic links

aide:
  kwargs:
    <<: *kwargs_common
    agent.search.max_debug_depth: 20000
"""
# Test to check if the agent.search.max_debug_depth overrides the kwargs_common value
import yaml

def test_max_debug_depth_override():
    data = yaml.safe_load(yaml_content)
    aide_kwargs = data['aide']['kwargs']
    print(data)
    assert aide_kwargs['agent.search.max_debug_depth'] == 20000, "Override failed"

test_max_debug_depth_override()
