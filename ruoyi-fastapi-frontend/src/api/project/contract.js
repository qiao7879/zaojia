import request from '@/utils/request'

export function listContract(query) {
  return request({
    url: '/project/contract/list',
    method: 'get',
    params: query
  })
}

export function getContract(contractId) {
  return request({
    url: '/project/contract/' + contractId,
    method: 'get'
  })
}

export function addContract(data) {
  return request({
    url: '/project/contract',
    method: 'post',
    data: data
  })
}

export function updateContract(data) {
  return request({
    url: '/project/contract',
    method: 'put',
    data: data
  })
}

export function delContract(contractId) {
  return request({
    url: '/project/contract/' + contractId,
    method: 'delete'
  })
}
